from Spaces import spaces, clear
import pickle
from os import remove
from os.path import exists

ACTIONS = ("menu", "interact", "inventory", "move")

menu_options = ["new", "quit"]
if exists("game.dat"):
	menu_options.append("save", "load")

class Player():
	def __init__(self):
		self.__position = [0, 0, 0]
		self.inventory = []
	
	@property
	def position(self):
		return self.__position
	
	@position.setter
	def position(self, new_position):
		self.__position = new_position


def valid_input(answer_set, prompt = "Input action:"):
	while (command := input(f"Possible inputs: {answer_set}\n{prompt} ").lower()) not in answer_set:
		print("Invalid input.")
	print()
	return command
	
def save():
	with open('game.dat','wb') as f:
		pickle.dump(player,f)
		pickle.dump(spaces,f)
	print("Game saved.")

def load():
	"""Loads the game data from game.dat"""
	global player
	global spaces

	try:
		with open("game.dat",'rb') as f:
			player = pickle.load(f)
			spaces = pickle.load(f)
		print("Game loaded.")
	except FileNotFoundError:
		print("Game file not found")

def game_loop():
	choice = None
	while choice != "menu":
		space = spaces.get(tuple(player.position), "There's not a space at that location. Code's broken.")
		print(space.description() + "\n")
		choice = valid_input(ACTIONS)
		match choice:
			case "move":
				space.move(player)
			case "interact":
				space.interact(player)
			case "inventory":
				print(f"Your inventory:\n{player.inventory}")
			case "menu":
				menu_options.append("resume")

player = Player()
def main(player):
	clear()
	choice = None
	while choice != "quit":
		print(""" _____    _____     ____     ____
|  __ \  |  __ \   / __ \   / ___\ 
| |__) | | |__) | | |  | | | | __
|  ___/  |  _  /  | |  | | | ||_ \ 
| |      | | \ \  | |__| | | |__| | 
|_|      |_|  \_\  \____/   \____/ 
""")
		choice = valid_input(menu_options, "Input option:")
		match choice:
			case "new":
				if exists("game.dat"):
					remove("game.dat")
				clear()
				print("You wake up and remember nothing besides a goal: to obtain the Prog.\n")
				game_loop()
			case "quit":
				print("Thanks for playing!")
			case "save":
				save()
			case "load":
				clear()
				load()
				game_loop()
			case "resume":
				game_loop()
				menu_options.pop()

if __name__ == "__main__":
	main(player)