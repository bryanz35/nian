import json

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
            print("Invalid direction")

    def look(self):
        print(rooms[self.location]["description"])
        print("Items in room: ")
        for item in rooms[self.location]["items"]:
            print(item)

    def take(self, item):
        if item in rooms[self.location]["items"]:
            self.inventory.append(item)
            rooms[self.location]["items"].remove(item)
        else:
            print("Item not found in room")

    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            rooms[self.location]["items"].append(item)
        else:
            print("Item not found in inventory")

name = input("Enter your name: ")
character = Player(name, "kitchen")

while True: 
    i = input().lower().split()
    match i[0]:
        case "go":
            character.move(i[1])
        case "look":
            character.look()
        case "quit":
            break
        case "take":
            character.take(i[1])
        case "get":
            character.take(i[1])
