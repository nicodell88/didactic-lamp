from pathlib import Path
import numpy as np
from enum import Enum
import collections
import plotly.graph_objects as go
import operator

class ColorDisp(Enum):
	GREY = "\U00002B1B"
	YELLOW = "\U0001F7E8"
	GREEN = "\U0001F7E9"

class ColorInt(Enum):
	GREY  = 0
	YELLOW = 1
	GREEN = 2

def create_look_up_table(word_list,n = None,disp = False):
	if n:
		word_list = word_list[:n]
	N = len(word_list)
	lookup_table = np.empty([N,N],dtype=np.uint8)

	for i,guess in enumerate(word_list):
		for j,answer in enumerate(word_list):

			encoding,pattern = calculate_pattern(guess, answer)
			lookup_table[i,j] = encoding
			if disp:
				print(f"Guess:  {guess}")
				print(f"Answer: {answer}")
				print(f"Pattern: {''.join(pattern)}")
				print(f"Encoding: {lookup_table[i,j]}")
				base3 = decimal2ternary(encoding)
				print(f"Base3: {base3}\n")
		print(f"{guess} - {i/N*100:.2f}%")

	return lookup_table

def calculate_pattern(guess, answer):
	pattern = [ColorDisp.GREY.value]*5
	guess_l = [char for char in guess]
	answ_l = [char for char in answer]
	encoding = np.uint8(0)
	for idx in range(5):
		if guess_l[idx] == answ_l[idx]:
			guess_l[idx] = '0'
			answ_l[idx]  = '-1'
			pattern[idx] = ColorDisp.GREEN.value
			encoding += ColorInt.GREEN.value*(3**idx)
	for idx in range(5):
		if guess_l[idx] in answ_l:
			idxx = answ_l.index(guess_l[idx])
			pattern[idx] =  ColorDisp.YELLOW.value
			answ_l[idxx] = '1'
			encoding += ColorInt.YELLOW.value*(3**idx)

	return encoding,''.join(pattern)

def calculate_entropy(lu):
	n_guess=lu.shape[0]
	n_answer=lu.shape[1]
	entropy_list = []
	for i in range(n_guess):
		frequency = collections.Counter(lu[i,:])
		entropy = 0

		for pat,cnt in frequency.items():
			p = cnt/n_answer
			# entropy -= p(x)log2(p(x))
			entropy += p*np.log2(1/p)
		# print(entropy)
		entropy_list.append(entropy)
	# print(max(entropy_list))
	# print(entropy_list.index(max(entropy_list)))
	return entropy_list

def decimal2ternary(n):
	if n == 0:
		return [0,0,0,0,0]
	nums = []
	while n:
		n, r = divmod(n, 3)
		nums.append(r)
	while len(nums) < 5:
		nums.append(0)
	return nums

def ternary2decimal(n):
	ans = 0
	for i,col in enumerate(n):
		ans+=col*3**i
	return ans

def decimal2pattern(n):
	n = decimal2ternary(n)
	colordict = {
		0:"\U00002B1B",
		1:"\U0001F7E8",
		2:"\U0001F7E9"
	}
	return ''.join([colordict[i] for i in n])


if __name__ == "__main__":
	filename="data/nytimes_all/words.txt"
	file1 = open(filename, 'r')

	word_list = file1.read().splitlines()
	file1.close()

	lu = create_look_up_table(word_list,n=None,disp=False)
	np.save("data/nytimes_all/lookuptable.npy", lu)
	assert False
	# lu = np.load("data/lookuptable.npy")
	entropy_list = calculate_entropy(lu)
	print(max(entropy_list))
	print(entropy_list.index(max(entropy_list)))
	

	print("max ent")
	idx = entropy_list.index(max(entropy_list))
	print(word_list[idx])
	print(entropy_list[idx])

	#First guess = weary
	idx_guess = word_list.index("weary")
	#First pattern = [1,2,0,0,0] = 7
	result_pattern = 6
	#find indicies where this is true
	idx_keep = np.where(lu[idx_guess,:]==result_pattern,True,False)
	#keep only these indicies from word list and from lu
	# lu = lu[:,idx_keep][idx_keep,:]
	# word_list = [word_list[i] for i,condition in enumerate(idx_keep.tolist())]
	
	entropy_list = calculate_entropy(lu)
	print(max(entropy_list))
	print(entropy_list.index(max(entropy_list)))
	

	print("max ent")
	idx = entropy_list.index(max(entropy_list))
	print(word_list[idx])
	print(idx)
	print(entropy_list[idx])
	print("\n")

	frequency = collections.Counter(lu[idx,:])
	x = []
	y = []
	for pat,cnt in frequency.items():
		x.append(pat.T)
		y.append(cnt)

	sorted_pairs = sorted(zip(x,y), key=operator.itemgetter(1))

	resorted = list(zip(*sorted_pairs))
	x=resorted[0]
	y=resorted[1]
	X = [str(i) for i in x]
	info = [decimal2pattern(i) for i in x]

	fig = go.Figure(data=[go.Bar(x=X,y=y, hovertemplate = "%{text}",text = info)])
	fig.show()

	print("min ent")
	idx = entropy_list.index(min(entropy_list))
	print(word_list[idx])
	print(idx)
	print(entropy_list[idx])

	frequency = collections.Counter(lu[idx,:])
	x = []
	y = []
	for pat,cnt in frequency.items():
		x.append(pat.T)
		y.append(cnt)

	sorted_pairs = sorted(zip(x,y), key=operator.itemgetter(1))

	resorted = list(zip(*sorted_pairs))
	x=resorted[0]
	y=resorted[1]
	X = [str(i) for i in x]
	info = [decimal2pattern(i) for i in x]

	fig = go.Figure(data=[go.Bar(x=X,y=y, hovertemplate = "%{text}",text = info)])
	fig.show()

