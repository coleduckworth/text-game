MOVEMENT = {"east" : 0,
			"north" : 1,
			"up" : 2,
			"west" : 3,
			"south" : 4,
			"down" : 5}

class Space():
	def __init__(self):
		self.allowed_movements = []
		self.descriptions = ""
	
	def description(self):
		return self.descriptions
	
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

class Interactable(Space):
	def __init__(self):
		super().__init__()
		self.usable_item = ""
		self.descriptions = {}
		self.affected_room = (0, 0, 0)
		self.state = "UNACTIVATED"
		self.interactable = True
	
	def description(self):
		return self.descriptions[self.state]
	
	def interact(self, player):
		if self.state == "UNACTIVATED" and self.interactable:
			if self.usable_item:
				print(f"Your inventory:\n{player.inventory}")
				item = input("You can use an item here.\nWhat item would you like to 'use'?\n").lower()
				if item in player.inventory:
					if item == self.usable_item:
						print(item)
						player.inventory.remove(item)
						self.state = "ACTIVATED"
						spaces[self.affected_room].state = "ACTIVE"
					else:
						print(f"You can't use {item} here.")
				else:
					print(f"You don't have {item} in your inventory.")
			else:
				self.state = "ACTIVATED"
				spaces[self.affected_room].state = "ACTIVE"
		elif self.state == "ACTIVATED":
			print("There's nothing to do here.")
		if self.state == "ACTIVE":
			self.action(player)
			self.state = "ACTIVATED"
	
	def action(self, player):
		pass

class Door(Interactable):
	def __init__(self):
		super().__init__()
		self.blocked_movement = ""

	def action(self, player):
		self.allowed_movements.append(self.blocked_movement)

class Dispenser(Interactable):
	def __init__(self):
		super().__init__()
		self.result_item = ""

	def action(self, player):
		print(f"You pickup the {self.result_item}.")
		player.inventory.append(self.result_item)

spaces = {}

s = Interactable()
s.affected_room = (0,2,0)
s.allowed_movements.append("north")
s.descriptions["UNACTIVATED"] = "unused"
s.descriptions["ACTIVATED"] = "used"
spaces[(0,0,0)] = s

s = Door()
s.affected_room = (0,1,0)
s.allowed_movements.append("south")
s.blocked_movement = "north"
s.descriptions["UNACTIVATED"] = "door"
s.descriptions["ACTIVATED"] = "opened door"
spaces[(0,1,0)] = s

s = Dispenser()
s.allowed_movements.append("south")
s.interactable = False
s.descriptions["UNACTIVATED"] = "other unused"
s.descriptions["ACTIVE"] = "There's a stick."
s.descriptions["ACTIVATED"] = "other used"
s.result_item = "stick"
spaces[(0,2,0)] = s
"""

s = Space()
s.allowed_movements.append("north")
"""