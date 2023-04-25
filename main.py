import Rooms

class Player():
	def __init__(self):
		self.__position = (0, 0, 0)
		self.inventory = []
	
	@property
	def position(self):
		return __position
	
	@position.setter
	def position(self, new):
		__position += new

def main(player):
	choice = None
	while choice != "quit":
		match choice:
			case "move":
				player.move()
