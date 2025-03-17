import json

rooms = open("rooms.json", "r")
items = open("items.json", "r")

rooms = json.load(rooms)
items = json.load(items)

while True: 
    i = input()