import numpy as np
import random
from myBot import utils
from pathlib import Path

data_folder = Path("data/nytimes_all")
# data_folder = Path("data/nytimes_answers")
# data_folder = Path("data/sbg-words")

class Game:
	def __init__(self,answer = None):
		word_file=data_folder/"words.txt"
		f = open(word_file, 'r')
		word_list = f.read().splitlines()
		f.close()

		self.lu = np.load(data_folder/"lookuptable.npy")

		self.word_list = sorted(word_list)
		self.still_playing = True

		if answer:
			assert answer in word_list
			self.answer = answer
		else:
			self.answer = False

	def entropy_list(self):
		return utils.calculate_entropy(self.lu)

	def guess(self,guess):
		if self.answer:
			if guess == self.answer:
				pattern = ''.join([utils.ColorDisp.GREEN.value]*5)
				self.still_playing = False
				return 242,pattern

		i = self.word_list.index(guess)
		j = self.word_list.index(self.answer)
		encoding = self.lu[i,j]
		pattern = utils.decimal2pattern(encoding)
		self.cull(guess,encoding)

		return encoding,pattern
	
	def cull(self,guess,encoding):
		idx_guess = self.word_list.index(guess)
		idx_keep = np.where(self.lu[idx_guess,:]==encoding,True,False)
		
		#keep only these indicies from word list and from lu
		self.lu = self.lu[:,idx_keep][idx_keep,:]
		self.word_list = [self.word_list[i] for i,condition in enumerate(idx_keep.tolist()) if condition]
		assert len(self.word_list) == self.lu.shape[0]
		assert len(self.word_list) == self.lu.shape[1]

	@property
	def N(self):
		return len(self.word_list)
	

def sim_game():
	wordle_answers = ["tacit"]
	# wordle_answers = ["swill","dodge","shake","caulk","aroma","cynic","robin","ultra","ulcer","pause","humor","frame","elder","skill","aloft","pleat","shard","moist","those","light","wrung","could","perky","mount","whack"]
	for soln in wordle_answers:
		print(f"\nNewGame\nAnswer = {soln}")
		game = Game(answer=soln)
		guesses = []
		patterns = []
		wordsleft = []
		while game.still_playing:
			if len(guesses) == 0:
					guess = "bears"
			elif len(game.word_list) >1:
				entropy_list = game.entropy_list()
				
				# sortedlist = sorted(entropy_list)	
				# sorted_idx = np.argsort(entropy_list)
				# n = min(10,sorted_idx.size)
				# idx = random.choices(
				# population=sorted_idx[-n:],
				# weights=sortedlist[-n:],
				# k=1)
				# guess = game.word_list[idx[0]]

				idx = entropy_list.index(max(entropy_list))
				guess = game.word_list[idx]
			else:
				guess = game.word_list[0]
			
			wordsleft.append(game.N)
			guesses.append(guess)
			encoding,pattern = game.guess(guess)
			patterns.append(pattern)
		print(f"            GUESS  WORDS REMAINING")
		for i in range(len(guesses)):
			print(f"{patterns[i]}  {guesses[i]}  {wordsleft[i]}")



if __name__ == "__main__":
	
	sim_game()

