MOVEMENT = {"east" : 0,
			"north" : 1
			"up" : 2
			"west" : 3
			"south" : 4
			"down" : 5}

class Space():
	def __init__(self):
		self.result_item = ""
		self.usable_item = ""
		self.allowed_movements = []
		self.description = ""
		self.__state = 0
	
	def move(self, player):
		print(f"You can go in the following directions:\n{self.allowed_movements}")
		direction = input("Which direction would you like to 'move'?\n")
		if direction in MOVEMENT:
			if direction in self.allowed_movements:
				print(f"You move {direction}.")
				direction = MOVEMENT[direction]
				if direction < 3:
					player.position[direction] += 1
				else:
					player.position[direction - 3] -= 1
			else:
				print(f"You can't move {direction} from here.")
		else:
			print(f"'{direction}' isn't a valid direction")
	
	def interact(self, player):
		if not self.__state:
			if self.usable_item:
				print(f"Your inventory:\n{player.inventory}")
				item = input("What item would you like to 'use'?\n").lower()
				if item in player.inventory:
					if item == self.usable_item:
						print(item)
						player.inventory.remove(item)
						self.usable_item = ""
						self.__state = 1
					else:
						print(f"You can't use {item} here.")
				else:
					print(f"You don't have {item} in your inventory.")
			else:

		else:
			print("There's nothing to interact with here.")