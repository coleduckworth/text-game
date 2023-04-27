import Spaces
import pickle

ACTIONS=("quit",
		 "save",
		 "load",
		 "interact",
		 "move")

class Player():
	def __init__(self):
		self.position = [0, 0, 0]
		self.inventory = []

def command():
	
def save():
	with open('game.dat','wb') as f:
		pickle.dump(player,f)
		pickle.dump(spaces,f)
	print("Game saved.")

def load():
	global player
	global spaces
	try:
		with open("game.dat",'rb') as f:
			player = pickle.load(f)
			spaces = pickle.load(f)
		print("Game loaded.")
	except FileNotFoundError:
		print("File not found.")

def main(player):
	choice = None
	space = spaces.get(player.position, "There's not a space at that location. Code's broken.")
	print(space.description)
	choice = command()
	while choice != "quit":
		match choice:
			case "move":
				space.move(player)
			case: "quit"
				save()
				print("Thanks for playing")
