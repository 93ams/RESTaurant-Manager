from database import session, Database
import json, requests

db = Database()
DEBUG = False

u1 = {
    "username": "tilau",
    "name": "andre",
    "password": "asd"
}
r = requests.post("http://localhost:7000/users", data=json.dumps(u1))

u2 = {
    "username": "mimi",
    "name": "princesa",
    "password": "dsa"
}
r = requests.post("http://localhost:7000/users", data=json.dumps(u2))

r1 = {
    "name": "castelo-da-mimi",
    "address": "praia cheia de chonchinhas 5 Dto",
    "first_manager": "mimi"
}
r = requests.post("http://localhost:7000/restaurants", data=json.dumps(r1))

r2 = {
    "name": "casa-bonita",
    "address": "Last of the mehicans St 94",
    "first_manager": "tilau"
}
r = requests.post("http://localhost:7000/restaurants", data=json.dumps(r2))

i1 = {
    "name": "bread",
    "type": "vegetarian"
}
r = requests.post("http://localhost:7000/ingredients", data=json.dumps(i1))

i2 = {
    "name": "meat",
    "type": "meat"
}
r = requests.post("http://localhost:7000/ingredients", data=json.dumps(i2))

i3 = {
    "name": "fillet",
    "type": "fish"
}
r = requests.post("http://localhost:7000/ingredients", data=json.dumps(i3))

i4 = {
    "name": "eggs",
    "type": "meat"
}
r = requests.post("http://localhost:7000/ingredients", data=json.dumps(i4))

i5 = {
    "name": "beans",
    "type": "vegetarian"
}
r = requests.post("http://localhost:7000/ingredients", data=json.dumps(i5))

d1 = {
    "name": "burrito",
    "cost": 2.99,
    "calories": 332,
    "ingredients": [i1["name"], i2["name"], i5["name"]]
}

r = requests.post("http://localhost:7000/restaurants/" + r1["name"] + "/dishes", data=json.dumps(d1))

d2 = {
    "name": "fish takito",
    "cost":  2.65,
    "calories": 156,
    "ingredients": [i1["name"], i3["name"]]
}
r = requests.post("http://localhost:7000/restaurants/" + r1["name"] + "/dishes", data=json.dumps(d2))

d3 = {
    "name": "burgers",
    "cost": 3.54,
    "calories":  619,
    "ingredients": [i1["name"], i2["name"], i4["name"]]
}
r = requests.post("http://localhost:7000/restaurants/" + r2["name"] + "/dishes", data=json.dumps(d3))

r = requests.delete("http://localhost:7000/ingredients/" + i1["name"])

db.dishes.add_ingredient(r2["name"], d3["name"], i4, new = True)
db.dishes.add_ingredient(r2["name"], d3["name"], i5["name"])

db.dishes.remove_ingredient(r1["name"], "burrito", i2["name"])

r = requests.delete("http://localhost:7000/restaurants/" + r1["name"] + "/dishes/" + d2["name"])

u = requests.get("http://localhost:7000/users")
try:
    print json.dumps(json.loads(u.text), indent=2)
except:
    print u.text

r = requests.get("http://localhost:7000/restaurants")
try:
    print json.dumps(json.loads(r.text), indent=2)
except:
    print r.text

d = requests.get("http://localhost:7000/dishes")
try:
    print json.dumps(json.loads(d.text), indent=2)
except:
    print d.text

i = requests.get("http://localhost:7000/ingredients")
try:
    print json.dumps(json.loads(i.text), indent=2)
except:
    print i.text

u = requests.get("http://localhost:7000/users/mimi")
try:
    print json.dumps(json.loads(u.text), indent=2)
except:
    print u.text

r = requests.get("http://localhost:7000/restaurants/casa-bonita")
try:
    print json.dumps(json.loads(r.text), indent=2)
except:
    print r.text

d = requests.get("http://localhost:7000/restaurants/casa-bonita/dishes/burgers")
try:
    print json.dumps(json.loads(d.text), indent=2)
except:
    print d.text

d = requests.get("http://localhost:7000/restaurants/casa-bonita/dishes")
try:
    print json.dumps(json.loads(d.text), indent=2)
except:
    print d.text

d = requests.get("http://localhost:7000/dishes/burrito")
try:
    print json.dumps(json.loads(d.text), indent=2)
except:
    print d.text

i = requests.get("http://localhost:7000/ingredients/beans")
try:
    print json.dumps(json.loads(i.text), indent=2)
except:
    print i.text

r = requests.delete("http://localhost:7000/restaurants")

r = requests.delete("http://localhost:7000/users")

r = requests.delete("http://localhost:7000/ingredients")

session.close()
