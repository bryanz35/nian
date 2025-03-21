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
        print("\nYou're in " + rooms[self.location]["description"])
        if len(rooms[self.location]["items"]) != 0:
            print("\nItems in room: ")
            for item in rooms[self.location]["items"]:
                print(item)
        else:
            print("\nThere doesn't seem to be any items in this room.")
        print("\nDirections you can go: ")
        for direction in rooms[self.location]["exits"]:
            print(direction)

    def inspect(self, item):
        if item in self.inventory:
            print(items[item]["description"])
        else:
            print("You don't have that item.")

    def take(self, item):
        if item in rooms[self.location]["items"]:
            self.inventory.append(item)
            rooms[self.location]["items"].remove(item)
            print("You took the " + item + " and placed it in your canvas bag.")
        else:
            print("Item not found in room.")

    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            rooms[self.location]["items"].append(item)
            print("You dropped the " + item + ".")
        else:
            print("Item not found in inventory.")

    def checkInv(self):
        print("You have:")
        for item in self.inventory:
            print(item)
        print("In your inventory.")

    def help(self):
        print("You can MOVE in a DIRECTION, LOOK, INSPECT an ITEM, TAKE an ITEM, CHECK your INVENTORY, get HELP, or DROP an ITEM.\n")

name = input("Enter your name: ")
character = Player(name, "kitchen")
print("\nYou find yourself back in your hometown. The Chinese New Year is arriving; how will you prepare this year?")
print("\nBright morning light shines through the window, you remember that you have much to prepare for.")
character.help()

while True: 
    print("\nWhat do you do next?")
    i = input().lower().split()
    if i == []:
        print("You can't just stand idly.")
        turns -= 1
        continue
    turns += 1
    match i[0]:
        case "go":
            character.move(i[1])
            character.look()
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
        case "check" | "inventory":
            character.checkInv()
        case _ :
            turns -= 1
            print("That action doesn't exist.")
    if turns == 33:
        print("\nThe sun is shining directly overhead. You get an ominous feeling.")
    elif turns == 66:
        print("\nIt's getting dark outside. Time is running out.")
    elif turns == 99:
        sum = 0
        for item in character.inventory:
            sum += item["value"]
        if sum > 20:
            print("\nThe unearthly beast has arrived at the town, but you are adequately prepared.")
            print("\nFaced with a sea of red decorations and unsettling noise, Nian backs off from your town.")
            print("\nYou've saved your friends and family from certain demise this year; how will you fair next New Year's Eve?")
            exit()
        else:
            print("\nThe unearthly beast has arrived at the town, wreaking havoc upon houses, families, and children.")
            print("\nMiraculously, you're one of the few spared by the supernatural disaster.")
            print("\nLeft with a town in shambles, you must work hard to rebuild everything your community has worked for.")
            print("\nNext year, will you be able to protect the things you love?.")
            exit()
        break