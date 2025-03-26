import json

global turns
global sum
turns = 0
points = 0
rooms = open("data/rooms.json", "r")
items = open("data/items.json", "r")

rooms = json.load(rooms)
items = json.load(items)
class Player:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.inventory = []
        self.health = 100
        self.gonged = False

    def move(self, direction):
        if direction in rooms[self.location]["exits"]:
            self.location = rooms[self.location]["exits"][direction]
            self.look()
        else:
            print("Invalid direction.")

    def look(self):
        print("\n" + rooms[self.location]["description"])
        if len(rooms[self.location]["items"]) != 0:
            print("\nItems in room: ")
            for item in rooms[self.location]["items"]:
                print(items[item]["name"])
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
        for room_item in rooms[self.location]["items"]:
            if item.lower() in items[room_item]["alias"] or item.lower() == items[room_item]["name"].lower():
                self.inventory.append(room_item)
                rooms[self.location]["items"].remove(room_item)
                print("You took the " + items[room_item]["name"] + " and placed it in your canvas bag.")
                return
        else:
            print("Item not found in room.")

    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            rooms[self.location]["items"].append(item)
            print("You dropped the " + item + ".")
        else:
            print("Item not found in inventory.")
    def use(self, item):
        for itemobject in items:
            if item in items[itemobject]["alias"]:
                # item is a valid thing. Now check inventory
                invSet = set(self.inventory)
                invSet.append(items[itemobject]["name"])
                #TODO
                if item == "Gong":
                    print("You hit the gong with the mallet. The sound reverberates through the air.")
                    if self.gonged == False:
                        print("You feel a little safer.")
                        points += 2
                        self.gonged = True
                    else:
                        print("Maybe you should stop. You'll get a noise complaint.")
                if item in rooms[self.location]["object_slots"]:
                    print("You placed the " + item + " in the room. What a wonderful decoration!")
                    rooms[self.location]["object_slots"].remove(item)
                    self.inventory.remove(item)
                    points += 1
                else:
                    print("You can't place that item here.")
                return
        print("You can't find that item in your inventory.")

    def checkInv(self):
        if len(self.inventory) == 0:
            print("You don't have anything in your inventory.")
        else:
            print("You have:")
            for item in self.inventory:
                print(item)
            print("In your inventory.")

    def light(self, item):
        
        if item in items["Unlit Lantern"]["alias"]:
            if "Old Flame Stick" in self.inventory and "Unlit Lantern" in self.inventory:
                
                self.inventory.remove("Unlit Lantern")
                self.inventory.append("Lit Lantern")
            else:
                print("\nYou don't have anything to light this lantern. Keep looking silly goose.")

        else:
            print("\nYou don't have anything to light yet. Are you an aspiring arsonist?")

    def help(self):
        print("You can MOVE in a DIRECTION, LOOK, INSPECT an ITEM, TAKE an ITEM, CHECK your INVENTORY, LIGHT items, get HELP, or DROP an ITEM.\n")

name = input("Enter your name: ")
character = Player(name, "Principal House")
print("\nYou find yourself back in your hometown. The Chinese New Year is arriving; how will you prepare this year?")
print("Bright morning light shines through the window, you remember that you have much to prepare for.")
character.help()

while True: 
    print("\nWhat do you do next?")
    i = input().lower().split()
    if i == []:
        print("You can't just stand idly.")
        turns -= 1
        continue
    turns += 1
    print("_____________________________________")
    match i[0]:
        case "go":
            character.move(i[1])
        case "look" | "l":
            character.look()
        case "quit" | "q":
            break
        case "take" | "get" | "grab":
            print("DEBUG: " + " ".join(i[1:]))
            character.take(" ".join(i[1:]))
        case "inspect" | "i":
            character.inspect(" ".join(i[1:]))
        case "drop" | "d":
            character.drop(" ".join(i[1:]))
        case "help" | "h":
            character.help()
        case "check" | "inventory":
            character.checkInv()
        case "light":
            character.light(" ".join(i[1:]))
        case "use":
            character.use(" ".join(i[1:]))
        case _ :
            turns -= 1
            print("That action doesn't exist.")
    if turns == 33:
        print("\nThe sun is shining directly overhead. You get an ominous feeling.")
    elif turns == 66:
        print("\nIt's getting dark outside. Time is running out.")
    elif turns == 99:
        if points > 5:
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