import numpy as np
import random
from myBot import utils
from pathlib import Path

import plotly.graph_objects as go


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

		self.answer_list = word_list
		self.guess_list = word_list
		self.still_playing = True

		if answer:
			assert answer in word_list
			self.answer = answer
		else:
			self.answer = False

	def entropy_list(self):
		return utils.calculate_entropy(self.lu)

	def guess(self,guess,cull_guess=True):
		if self.answer:
			if guess == self.answer:
				pattern = ''.join([utils.ColorDisp.GREEN.value]*5)
				self.still_playing = False
				return 242,pattern

		i = self.guess_list.index(guess)
		j = self.answer_list.index(self.answer)
		encoding = self.lu[i,j]
		pattern = utils.decimal2pattern(encoding)
		self.cull(guess,encoding,cull_guess=cull_guess)

		return encoding,pattern
	
	def cull(self,guess,encoding,cull_guess=True):
		idx_guess = self.guess_list.index(guess)
		idx_keep = np.where(self.lu[idx_guess,:]==encoding,True,False)
		
		#keep only these indicies from word list and from lu
		self.lu = self.lu[:,idx_keep]
		# self.lu = self.lu[:,idx_keep][idx_keep,:]
		self.answer_list = [self.answer_list[i] for i,condition in enumerate(idx_keep.tolist()) if condition]
		assert len(self.answer_list) == self.lu.shape[1]
		assert len(self.guess_list) == self.lu.shape[0]


		if cull_guess:
			idx_keep = [self.guess_list[i] in self.answer_list for i in range(len(self.guess_list))]
			self.lu = self.lu[idx_keep,:]
			self.guess_list = [self.guess_list[i] for i,condition in enumerate(idx_keep) if condition]
			assert len(self.answer_list) == self.lu.shape[1]
			assert len(self.guess_list) == self.lu.shape[0]
	@property
	def N(self):
		return len(self.answer_list)
	

def sim_game():
	wordle_answers = ["cigar", "rebut", "sissy", "humph", "awake", "blush", "focal", "evade", "naval", "serve", "heath", "dwarf", "model", "karma", "stink", "grade", "quiet", "bench", "abate", "feign", "major", "death", "fresh", "crust", "stool", "colon", "abase", "marry", "react", "batty", "pride", "floss", "helix", "croak", "staff", "paper", "unfed", "whelp", "trawl", "outdo", "adobe", "crazy", "sower", "repay", "digit", "crate", "cluck", "spike", "mimic", "pound", "maxim", "linen", "unmet", "flesh", "booby", "forth", "first", "stand", "belly", "ivory", "seedy", "print", "yearn", "drain", "bribe", "stout", "panel", "crass", "flume", "offal", "agree", "error", "swirl", "argue", "bleed", "delta", "flick", "totem", "wooer", "front", "shrub", "parry", "biome", "lapel", "start", "greet", "goner", "golem", "lusty", "loopy", "round", "audit", "lying", "gamma", "labor", "islet", "civic", "forge", "corny", "moult", "basic", "salad", "agate", "spicy", "spray", "essay", "fjord", "spend", "kebab", "guild", "aback", "motor", "alone", "hatch", "hyper", "thumb", "dowry", "ought", "belch", "dutch", "pilot", "tweed", "comet", "jaunt", "enema", "steed", "abyss", "growl", "fling", "dozen", "boozy", "erode", "world", "gouge", "click", "briar", "great", "altar", "pulpy", "blurt", "coast", "duchy", "groin", "fixer", "group", "rogue", "badly", "smart", "pithy", "gaudy", "chill", "heron", "vodka", "finer", "surer", "radio", "rouge", "perch", "retch", "wrote", "clock", "tilde", "store", "prove", "bring", "solve", "cheat", "grime", "exult", "usher", "epoch", "triad", "break", "rhino", "viral", "conic", "masse", "sonic", "vital", "trace", "using", "peach", "champ", "baton", "brake", "pluck", "craze", "gripe", "weary", "picky", "acute", "ferry", "aside", "tapir", "troll", "unify", "rebus", "boost", "truss", "siege", "tiger", "banal", "slump", "crank", "gorge", "query", "drink", "favor", "abbey", "tangy", "panic", "solar", "shire", "proxy", "point", "robot", "prick", "wince", "crimp", "knoll", "sugar", "whack", "mount", "perky", "could", "wrung", "light", "those", "moist", "shard", "pleat", "aloft", "skill", "elder", "frame", "humor", "pause", "ulcer", "ultra", "robin", "cynic", "aroma", "caulk", "shake", "dodge", "swill","tacit","other","thorn","trove","bloke","vivid","spill","chant","choke"]
	# wordle_answers = ["boozy"]#pathelogical example
	
	score = []
	for soln in wordle_answers:
		print(f"\nNewGame\nAnswer = {soln}")
		game = Game(answer=soln)
		guesses = []
		patterns = []
		wordsleft = []
		valid = []
		while game.still_playing:
			if len(guesses) == 0:
					guess = "tares"
			elif game.N >1:
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
				guess = game.guess_list[idx]
			else:
				guess = game.answer_list[0]
			
			wordsleft.append(game.N)
			guesses.append(guess)
			v = "\U00002705" if (guess in game.answer_list) else "\U000026D4"
			valid.append(v)
			encoding,pattern = game.guess(guess,cull_guess = len(guesses)>1 )
			patterns.append(pattern)
		print(f"            GUESS  WORDS REMAINING")
		for i in range(len(guesses)):
			print(f"{patterns[i]}  {guesses[i]}{valid[i]}  {wordsleft[i]}")
		score.append(len(guesses))

	return score



if __name__ == "__main__":
	
	score = sim_game()

	fig = go.Figure(data=[go.Histogram(x=score)])
	fig.update_layout(
    title_text='Sacrificial Guess - Maximum Entropy', # title of plot
    xaxis_title_text='Score', # xaxis label
    yaxis_title_text='Count', # yaxis label
    bargap=0.2, # gap between bars of adjacent location coordinates
    bargroupgap=0.1 # gap between bars of the same location coordinates
)
	fig.show()

