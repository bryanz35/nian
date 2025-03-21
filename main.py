import json

global turns
turns = 0
rooms = open("data/rooms.json", "r")
items = open("data/items.json", "r")

rooms = json.load(rooms)
items = json.load(items)
print(rooms)
print(items)
class Player:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.inventory = []
        self.health = 100

    def move(self, direction):
        if direction in rooms[self.location]["exits"]:
            self.location = rooms[self.location]["exits"][direction]
            self.look()
        else:
            print("Invalid direction.")

    def look(self):
        print("You're in " + rooms[self.location]["description"])
        print("\nItems in room: ")
        for item in rooms[self.location]["items"]:
            print(item)
        print("\nDirections you can go: ")
        for direction in rooms[self.location]["exits"]:
            print(direction)

    def inspect(self, item):
        if item in self.inventory:
            print(item["description"])
        else:
            print("You don't have that item.")

    def take(self, item):
        if item in rooms[self.location]["items"]:
            self.inventory.append(item)
            rooms[self.location]["items"].remove(item)
        else:
            print("Item not found in room.")

    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            rooms[self.location]["items"].append(item)
        else:
            print("Item not found in inventory.")

    def help(self):
        print("You can MOVE in a DIRECTION, LOOK, INSPECT and ITEM, TAKE an ITEM, or DROP an ITEM.\n")

name = input("Enter your name: ")
character = Player(name, "kitchen")
print("\nYou find yourself back in your hometown. The Chinese New Year is arriving; how will you prepare this year?")
print("\nBright morning light shines through the window, you remember that you have much to prepare for.")
character.help()

while True: 
    character.look()
    print("What do you do next?")
    while True:
        i = input().lower().split()
        if i == []:
            print("You can't just stand idly.")
        else:
            break
    turns += 1
    match i[0]:
        case "go":
            character.move(i[1])
        case "look" | "l":
            character.look()
        case "quit" | "q":
            break
        case "take" | "get" | "grab":
            character.take(i[1])
        case "inspect" | "i":
            character.inspect(i[1])
        case "drop" | "d":
            character.drop(i[1])
        case "help" | "h":
            character.help()
        case _ :
            print("That action doesn't exist.")
    if turns == 33:
        print("\nThe sun is shining directly overhead. You get an uneasy feeling in your chest.")
    elif turns == 66:
        print("\nIt's getting dark outside. Time is running out.")
    elif turns == 99:
        break