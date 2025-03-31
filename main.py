import json

global sum

rooms = open("data/rooms.json", "r")
items = open("data/items.json", "r")

rooms = json.load(rooms)
items = json.load(items)
class Player:
    def __init__(self, location):
        self.location = location
        self.inventory = []
        self.health = 100
        self.gonged = False
        self.points = 0
        self.turns = 0

    def move(self, direction):
        if direction in rooms[self.location]["exits"]:
            self.location = rooms[self.location]["exits"][direction]
            self.look()
        else:
            print("Invalid direction.")
            self.turns -= 1

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
        for itemobject in items:
            if item in items[itemobject]["alias"]:
                invSet = set(self.inventory)
                invSet.add(items[itemobject]["name"])
                if len(invSet) < len(self.inventory) + 1:
                    print(items[itemobject]["description"])
                else:
                    print("You don't have that item.")
                    self.turns -= 1

    def take(self, item):
        for room_item in rooms[self.location]["items"]:
            if item == "kids" or item == "children":
                print("You hear sirens approaching. Maybe not a good idea.")
            if item.lower() in items[room_item]["alias"] or item.lower() == items[room_item]["name"].lower():
                self.inventory.append(room_item)
                rooms[self.location]["items"].remove(room_item)
                print("You took the " + items[room_item]["name"] + " and placed it in your canvas bag.")
                return
        else:
            print("Item not found in room.")
            self.turns -= 1

    def drop(self, item):
        for itemobject in items:
            if item in items[itemobject]["alias"]:
                invSet = set(self.inventory)
                invSet.add(items[itemobject]["name"])
                if len(invSet) < len(self.inventory) + 1:
                    print("You drop the " + items[itemobject]["name"] + " on the ground.")
                    self.inventory.remove(itemobject)
                    rooms[self.location]["items"].append(itemobject)
                else:
                    print("You don't have that item.")
                    self.turns -= 1

    def use(self, item):
        for itemobject in items:
            if item in items[itemobject]["alias"]:
                invSet = set(self.inventory)
                invSet.add(items[itemobject]["name"])
                if len(invSet) < len(self.inventory) + 1:
                    if itemobject == "Gong":
                        print("You hit the gong with the mallet. The sound reverberates through the air.")
                        if self.gonged == False:
                            print("You feel a little safer.")
                            self.points += 2
                            self.gonged = True
                        else:
                            print("Maybe you should stop. You'll get a noise complaint.")
                            self.turns -= 1
                        return
                    
                    if itemobject in rooms[self.location]["object_slots"]:
                        if itemobject == "Dragon's Eye":
                            print("The dragon's eye fits smoothly into the eye of nian.")
                            print("You hear a low rumble")
                            print("Suddenly, it becomes nighttime!")
                            self.turns = 50
                            return
                        if itemobject == "Firecracker":
                            print("You use the firecracker, spreading the holiday joy. This will probably scare nian!")
                            self.inventory.remove(itemobject)
                            self.points += 1
                            return
                        print("You placed the " + itemobject + " in the room. What a wonderful decoration!")
                        rooms[self.location]["object_slots"].remove(itemobject)
                        self.inventory.remove(itemobject)
                        self.points += 1
                    elif itemobject in items["Unlit Lantern"]["alias"]:
                        if "Lit Lantern" in self.inventory:
                            self.use("lit lantern")
                            return
                        print("Hanging up an unlit lantern seems depressing. Maybe there's a way to light it?")
                        self.turns -= 1
                    else:
                        print("You can't place that item here. Maybe it'll fit somewhere else...")
                        self.turns -= 1
                    return
        print("You can't find that item in your inventory.")
        self.turns -= 1

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
                print("The lantern glows with a soft brilliance. You feel the desire to hang it up.")
            else:
                print("\nYou don't have anything to light this lantern with. Keep looking silly goose.")
                self.turns -= 1

        else:
            print("\nYou don't have anything to light yet. Are you an aspiring arsonist?")
            self.turns -= 1

    def help(self):
        print("You can MOVE in a DIRECTION, LOOK, INSPECT an ITEM, TAKE an ITEM, \nCHECK your INVENTORY, LIGHT items, get HELP, or DROP an ITEM.\n")

character = Player("Principal House")
print("\nYou find yourself back in your hometown. The Chinese New Year is arriving; how will you prepare this year?")
print("Bright morning light shines through the window, you remember that you have much to prepare for.")
character.help()

while True: 
    print("\nWhat do you do next?")
    character.turns += 1
    i = input().lower().split()
    if i == []:
        print("You can't just stand idly.")
        character.turns -= 1
        continue
    print("_____________________________________")
    match i[0]:
        case "go" | "move":
            if len(i) == 1:
                print("Be more specific.")
                character.turns -= 1
                continue
            character.move(i[1])
        case "look" | "l":
            character.look()
        case "quit" | "q":
            break
        case "take" | "get" | "grab":
            if len(i) == 1:
                print("Be more specific.")
                character.turns -= 1
                continue
            character.take(" ".join(i[1:]))
        case "inspect" | "i":
            if len(i) == 1:
                print("Be more specific.")
                character.turns -= 1
                continue
            character.inspect(" ".join(i[1:]))
        case "drop" | "d":
            if len(i) == 1:
                print("Be more specific.")
                character.turns -= 1
                continue
            character.drop(" ".join(i[1:]))
        case "help" | "h":
            character.help()
        case "check" | "inventory":
            character.checkInv()
        case "light":
            if len(i) == 1:
                print("Be more specific.")
                character.turns -= 1
                continue
            character.light(" ".join(i[1:]))
        case "use":
            if len(i) == 1:
                print("Be more specific.")
                character.turns -= 1
                continue
            character.use(" ".join(i[1:]))
        case _ :
            character.turns -= 1
            print("That action doesn't exist.")
    if character.turns == 20:
        print("\nThe sun is shining directly overhead. You get an ominous feeling.")
    elif character.turns == 40:
        print("\nIt's getting dark outside. Time is running out.")
    elif character.turns >= 50:
        if character.points > 5:
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