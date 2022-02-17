from pathlib import Path
import numpy as np
from enum import Enum
import collections
import plotly.graph_objects as go
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
			pattern = [ColorDisp.GREY.value]*5
			guess_l = [char for char in guess]
			answ_l = [char for char in answer]
			encoding = np.uint8(0)
			for idx in range(5):
				if guess_l[idx] == answ_l[idx]:
					pattern[idx] = ColorDisp.GREEN.value
					answ_l[idx] = "0"
					encoding += ColorInt.GREEN.value*(3**idx)
				elif guess_l[idx] in answ_l:
					idxx = answ_l.index(guess_l[idx])
					pattern[idx] =  ColorDisp.YELLOW.value
					answ_l[idxx] = "0"
					encoding += ColorInt.YELLOW.value*(3**idx)
			
			lookup_table[i,j] = encoding
			if disp:
				print(f"Guess:  {guess}")
				print(f"Answer: {answer}")
				print(f"Pattern: {''.join(pattern)}")
				# print(f"Encoding: {encoding}")
				print(f"Encoding: {lookup_table[i,j]}\n")
		
		print(f"{i/N*100:.2f}%")

	return lookup_table
	
def calculate_entropy(lu):
	N=lu.shape[0]
	entropy_list = []
	for i in range(N):
		frequency = collections.Counter(lu[i,:])
		entropy = 0

		for pat,cnt in frequency.items():
			p = cnt/N
			# entropy -= p(x)log2(p(x))
			entropy += p*np.log2(1/p)
		# print(entropy)
		entropy_list.append(entropy)
	# print(max(entropy_list))
	# print(entropy_list.index(max(entropy_list)))
	return entropy_list




if __name__ == "__main__":
	# print("\U00002B1B\U0001F7E6\U0001F7E7\U0001F7E8\U0001F7E9")
	filename="data/words.txt"
	file1 = open(filename, 'r')
	word_list = file1.read().splitlines()
	# lu = create_look_up_table(word_list,n=600,disp=False)
	# np.save("data/lookuptable.npy", lu)
	lu = np.load("data/lookuptable.npy")
	entropy_list = calculate_entropy(lu)
	print(max(entropy_list))
	print(entropy_list.index(max(entropy_list)))
	

	print("max ent")
	idx = entropy_list.index(max(entropy_list))
	print(word_list[idx])
	print(entropy_list[idx])

	fig = go.Figure(data=[go.Histogram(x=lu[:,idx])])
	fig.show()



	print("min ent")
	idx = entropy_list.index(min(entropy_list))
	print(word_list[idx])
	print(entropy_list[idx])

	fig = go.Figure(data=[go.Histogram(x=lu[:,idx])])
	fig.show()






