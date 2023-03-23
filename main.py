class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, direction):
        match direction:
            case "up":
                self.y -= 1
            case "down":
                self.y += 1
            case "left":
                self.x -= 1
            case "right":
                self.x += 1

class Map():
    def __init__(self, map):
        self.map = map

    def __str__(self):
        res = []
        for i in self.map:
            res.append(i)
        res = "\n".join(res)
        return res

class Interactable():
    def __init__(self, interactText, neededItem = None, resultingItem = None):
        self.interactText = interactText
        self.neededItem = neededItem
        self.resultingItem = resultingItem
    
floor1 = Map([
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ['|', ' ', ' ', '|', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
    ['|', '-', ' ', '|', ' ', ' ', ' ', ' ', '|', ' ', ' ', '|', ' ', '-', '-', '|', ' ', '|'],
    ['|', ' ', ' ', '|', ' ', ' ', ' ', ' ', '|', ' ', ' ', '|', ' ', ' ', ' ', '|', ' ', '|'],
    ['|', '-', ' ', '|', '-', '-', '-', ' ', '|', '-', '-', '|', ' ', '-', '-', '|', ' ', '|'],
    ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', '|'],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']])

print(floor1)

