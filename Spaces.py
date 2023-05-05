from os import system

MOVEMENT = {"east" : 0,
			"north" : 1,
			"up" : 2,
			"west" : 3,
			"south" : 4,
			"down" : 5}

def clear():
	system("cls")
	#system("clear")

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
				clear()
			else:
				print(f"You can't move {direction} from here.")
		else:
			print(f"'{direction}' isn't a valid direction")

class Interactable(Space):
	def __init__(self):
		super().__init__()
		self.usable_item = ""
		self.answer = ""
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
						player.inventory.remove(item)
						self.state = "ACTION"
						print(self.description())
						self.state = "ACTIVATED"
						spaces[self.affected_room].state = "ACTIVE"
					else:
						print(f"You can't use {item} here.")
				else:
					print(f"You don't have {item} in your inventory.")
			elif self.answer:
				guess = input("You can input text here.\nInput text:\n").lower()
				if guess == self.answer:
					self.state = "ACTION"
					print(self.description())
					self.state = "ACTIVATED"
					spaces[self.affected_room].state = "ACTIVE"
				else:
					print("Your response was erased and nothing occurred.")
			else:
				self.state = "ACTION"
				print(self.description())
				self.state = "ACTIVATED"
				spaces[self.affected_room].state = "ACTIVE"
		elif self.state == "ACTIVATED" or not self.interactable:
			print("There's nothing to do here.")
		if self.state == "ACTIVE":
			self.state = "ACTIVATED"
			self.action(player)
	
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

s = Space()
s.allowed_movements = ["north", "south"]
s.descriptions = "You see a cold stone cell. There's a door to the north and a wooden bed to the south."
spaces[(0,0,0)] = s

s = Dispenser()
s.allowed_movements.append("north")
s.affected_room = (0,-1,0)
s.descriptions["UNACTIVATED"] = "You see an uncomfortable looking bed. A thin blanket is neatly spread across the top."
s.descriptions["ACTION"] = "You pull off the blanket to reveal a key."
s.descriptions["ACTIVATED"] = "You see an uncomfortable looking bed. A thin blanket is crumpled on top of it."
s.result_item = "key"
spaces[(0,-1,0)] = s

s = Door()
s.allowed_movements.append("south")
s.affected_room = (0,1,0)
s.usable_item = "key"
s.descriptions["UNACTIVATED"] = "You see a locked iron door. Despite this seeming to be a prison cell, there is a keyhole on the inside."
s.descriptions["ACTION"] = "You unlock the door, but you can't pull the key out of the keyhole."
s.descriptions["ACTIVATED"] = "You see an opened iron door."
s.blocked_movement = "north"
spaces[(0,1,0)] = s

s = Space()
s.allowed_movements = ["east", "west", "south"]
s.descriptions = "You see a dim corridor lit only by a glow coming from the cracks around a door to the east. The corrider also extends to the west, ending at a door with a plaque.\nThe door to the south connects to a prison cell."
spaces[(0,2,0)] = s

s = Door()
s.allowed_movements = ["west"]
s.interactable = False
s.descriptions["UNACTIVATED"] = "You see a door surrounded by a pulsating green light. The door is a flat cast iron slab and noticably lacks a handle."
s.descriptions["ACTIVE"] = "You see a door surrounded by a pulsating green light. The door is a flat cast iron slab save for a small crevasse that your hand may fit into.\n"
s.descriptions["ACTION"] = "You put your hand into the crevasse and pull the heavy slab to the side, flooding the corridor with green light."
s.descriptions["ACTIVATED"] = "You see a cast iron slab slid to the side, revealing an entryway. Green light floods in from a stone room."
s.blocked_movement = "east"
spaces[(1,2,0)] = s

s = Door()
s.allowed_movements = ["east"]
s.affected_room = (-1,2,0)
s.answer = "green"
s.descriptions["UNACTIVATED"] = "You see a wooden door with a plaque on it. The plaque is only barely illuminated from the light coming from the other end of the hall.\nThe plaque says:\nWhat color does my friend to the east shine with?"
s.descriptions["ACTION"] = "The plaque disintegrates and the door swings open."
s.descriptions["ACTIVATED"] = "You see an opened wooden door. The area is dimly lit by the light coming from the other end of the hall."
s.blocked_movement = "west"
spaces[(-1,2,0)] = s

s = 