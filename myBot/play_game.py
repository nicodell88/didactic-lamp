
from myBot import utils
from myBot import simulate_game
import operator

class AssistHuman:
	def __init__(self):
		self.game = simulate_game.Game()
	
	def play(self):
		print("Let's Play!")
		k = 0
		while len(self.game.answer_list)>1:
			sorted_pairs = sorted(zip(self.game.guess_list,self.game.entropy_list()), key=operator.itemgetter(1),reverse=True)
			print("Word   Entropy  Valid")
			for i,pair in enumerate(sorted_pairs):
				print(f"{pair[0]} {pair[1]} {pair[0] in self.game.answer_list}")
				if i>=100:
					break
			
			print("What word would you like to guess?")
			guess = input(">>>")
			print(f"You've guessed {guess}")
			print("What was the wordle response?")
			response = input(">>>")
			t = [int(r) for r in response]
			dec = utils.ternary2decimal(t)
			pat = utils.decimal2pattern(dec)
			print(f"Wordle responded with {pat}")

			cull_guess = k>0
			k+=1
			self.game.cull(guess,dec,cull_guess=True)

			if self.game.N ==1 and self.game.answer_list[0] == guess:
				print("Congratulations!")
				break
			elif self.game.N ==1:
				print(f"There is only 1 possible remaining answer: {self.game.answer_list[0]}")
			else:
				print(f"There are {self.game.N} possible answers remaining.")

			if self.game.N ==0:
				print("Wordle answer might not be in our list")
				break
			



if __name__ == "__main__":
	game =  AssistHuman()
	game.play()