from os import system

MOVEMENT = {"east" : 0,
			"north" : 1,
			"up" : 2,
			"west" : 3,
			"south" : 4,
			"down" : 5}

def clear():
	#system("cls")
	system("clear")

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
		self.usable_items = []
		self.answers = []
		self.descriptions = {}
		self.affected_room = (0, 0, 0)
		self.state = "UNACTIVATED"
		self.interactable = True
	
	def description(self):
		return self.descriptions[self.state]
	
	def interact(self, player):
		if self.state == "UNACTIVATED" and self.interactable:
			if self.usable_items:
				print(f"Your inventory:\n{player.inventory}")
				item = input("You can use an item here.\nWhat item would you like to 'use'?\n").lower()
				if item in player.inventory:
					if item in self.usable_items:
						player.inventory.remove(item)
						self.usable_items.remove(item)
						if self.usable_items:
							print(self.descriptions["PROGRESS"])
						else:
							print(self.descriptions["ACTION"])
							self.state = "ACTIVATED"
							spaces[self.affected_room].state = "ACTIVE"
					else:
						print(f"You can't use {item} here.")
				else:
					print(f"You don't have {item} in your inventory.")
			elif self.answers:
				guess = input("You can input text here.\nInput text:\n").lower()
				if guess in self.answers:
					print(self.descriptions["ACTION"])
					self.state = "ACTIVATED"
					spaces[self.affected_room].state = "ACTIVE"
				else:
					print("Your response was erased and nothing occurred.")
			else:
				print(self.descriptions["ACTION"])
				self.state = "ACTIVATED"
				spaces[self.affected_room].state = "ACTIVE"
		elif self.state == "ACTIVATED" or (not self.interactable and self.state == "ACTIVE"):
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
s.usable_items = ["key"]
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
s.descriptions["ACTIVATED"] = "You see a cast iron slab slid to the side, revealing an entryway. Light floods in from a painted room."
s.blocked_movement = "east"
spaces[(1,2,0)] = s

s = Door()
s.allowed_movements = ["east"]
s.affected_room = (-1,2,0)
s.answers = ["green"]
s.descriptions["UNACTIVATED"] = "You see a wooden door with a plaque on it. The plaque is only barely illuminated from the light coming from the other end of the hall.\nThe plaque says:\nWhat color does my friend to the east shine with?"
s.descriptions["ACTION"] = "The plaque disintegrates and the door swings open."
s.descriptions["ACTIVATED"] = "You see an opened wooden door. The area is dimly lit by the light coming from the other end of the hall."
s.blocked_movement = "west"
spaces[(-1,2,0)] = s

s = Interactable()
s.allowed_movements = ["east"]
s.affected_room = (1,2,0)
s.answers = ["a shadow", "shadow", "shadows"]
s.descriptions["UNACTIVATED"] = "You see a small pad of paper on a table. Written upon it is a riddle:\nI can only live where there is light but if a light shines on me, I die. What am I?"
s.descriptions["ACTION"] = "All text is removed from the pad and you can hear metal grinding against stone behind you."
s.descriptions["ACTIVATED"] = "You see a small pad of paper on a table. Upon closer inspection it is blank."
spaces[(-2,2,0)] = s

s = Interactable()
s.allowed_movements = ["north, east, south, west"]
s.affected_room = (2,2,0)
s.answers = ["red"]
s.descriptions["UNACTIVATED"] = "You see a small room completely colored yellow. A singular light source is embedded in the ceiling above you glowing bright green.\nYou can see a door to your north, a dim hallway to your west, and two other brightly colored rooms to your east and south.\nA plaque on the wall reads:\nWhat color am I painted?"
s.descriptions["ACTION"] = "The plaque disappears and a seemingly yellow key falls from the ceiling. The light source changes to shine white."
s.descriptions["ACTIVATED"] = "You see a small room completely colored red. A singular light source is embedded in the ceiling above you glowing bright white.\nYou can see a door to your north, a dim hallway to your west, and two other brightly colored rooms to your east and south."
s.result_item = "red key"
spaces[(2,2,0)] = s

s = Interactable()
s.allowed_movements = ["south, west"]
s.affected_room = (3,2,0)
s.answers = ["blue"]
s.descriptions["UNACTIVATED"] = "You see a small room completely colored purple. A singular light source is embedded in the ceiling above you glowing bright red.\nYou can see two other brightly colored rooms to your west and south.\nA plaque on the wall reads:\nWhat color am I painted?"
s.descriptions["ACTION"] = "The plaque disappears and a seemingly purple key falls from the ceiling. The light source changes to shine white."
s.descriptions["ACTIVATED"] = "You see a small room completely colored blue. A singular light source is embedded in the ceiling above you glowing bright white.\nYou can see two other brightly colored rooms to your west and south."
s.result_item = "blue key"
spaces[(3,2,0)] = s

s = Interactable()
s.allowed_movements = ["north, east"]
s.affected_room = (2,1,0)
s.answers = ["green"]
s.descriptions["UNACTIVATED"] = "You see a small room completely colored cyan. A singular light source is embedded in the ceiling above you glowing bright blue.\nYou can see two other brightly colored rooms to your north and east.\nA plaque on the wall reads:\nWhat color am I painted?"
s.descriptions["ACTION"] = "The plaque disappears and a seemingly cyan key falls from the ceiling. The light source changes to shine white."
s.descriptions["ACTIVATED"] = "You see a small room completely colored green. A singular light source is embedded in the ceiling above you glowing bright white.\nYou can see two other brightly colored rooms to your north and east."
s.result_item = "green key"
spaces[(2,1,0)] = s

s = Interactable()
s.allowed_movements = ["north, west"]
s.affected_room = (3,1,0)
s.answers = ["white"]
s.descriptions["UNACTIVATED"] = "You see a small room completely colored purple. A singular light source is embedded in the ceiling above you glowing bright purple.\nYou can see two other brightly colored rooms to your north and west.\nA plaque on the wall reads:\nWhat color am I painted?"
s.descriptions["ACTION"] = "The plaque disappears and a seemingly purple key falls from the ceiling. The light source changes to shine white."
s.descriptions["ACTIVATED"] = "You see a small room completely colored white. A singular light source is embedded in the ceiling above you glowing bright white.\nYou can see two other brightly colored rooms to your north and west."
s.result_item = "white key"
spaces[(3,1,0)] = s

s = Door()
s.allowed_movements = ["south"]
s.affected_room = (2,3,0)
s.usable_items = ["red key", "blue key", "green key", "white key"]
s.descriptions["UNACTIVATED"] = "You see a simple metal door with four keyholes."
s.descriptions["PROGRESS"] = "The key turns in a keyhole and is unable to be removed."
s.descriptions["ACTION"] = "The door unlocks and you push it open."
s.descriptions["ACTIVATED"] = "You see an open door. Beyond the door is a completely dark room."
s.blocked_movement = "north"
spaces[(2,3,0)] = s

s = Space()
s.allowed_movements = ["down"]
s.descriptions = "You fall into a pit hidden in the darkness."
spaces[(2,4,0)] = s
"""
for i in range(len("Message"[::-1])):
	s = Space()
	s.allowed_movements = ["down"]
	s.descriptions = f"You fall in a pitch black abyss. You see in the darkness the letter \"{("Message"[-1-i])}\""
	spaces[(2,4,0 - i)] = s

s = Space()
s.allowed_movements = [""]
"""