from Spaces import spaces, clear, Interactable
import pickle
from os import remove
from os.path import exists

win = False
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

def win_screen():
	clear()
	print("You walk into the darkness and stop. You can sense the Prog. You reach out and grab it. Your fingers wrap around it and, for a moment, your mind is filled with unbearable ecstasy.\nAnd then...\nNothing.\nYou realize that you can never feel that way again.\nYour life becomes so devoid of purpose that you black out.\n")
	input("PRESS ENTER")
	clear()
	print("Thank you for playing PROG.\n\tCREDITS\n\nCreated by Cole Duckworth\n\nSpecial thanks to Mr. Simonsen\n")
	input("PRESS ENTER")
	clear()

def game_loop():
	choice = None
	while choice != "menu":
		space = spaces.get(tuple(player.position), "There's not a space at that location. Code's broken.")
		if space.description() == "PROG":
			choice = "menu"
			global win
			win = True
		else:
			print("\n" + space.description() + "\n")
			actions = ["menu", "inventory", "move"]
			if isinstance(space, Interactable):
				actions.append("interact")
			choice = valid_input(actions)
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
	choice = None
	while choice != "quit" and not win:
		clear()
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
				print("You wake up and remember nothing besides a goal: to obtain the Prog.")
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
	if win:
		win_screen()

if __name__ == "__main__":
	main(player)