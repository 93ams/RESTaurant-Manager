from database import User, Restaurant, Dish, Ingredient, session, Database
import json, os

db = Database()

u1 = {
    "username": "tilau",
    "name": "andre",
    "password": "asd"
}
db.users.insert(u1)

u2 = {
    "username": "mimi",
    "name": "princesa",
    "password": "dsa"
}
db.users.insert(u2)

r1 = {
    "name": "castelo da mimi",
    "address": "praia cheia de chonchinhas 5 Dto",
    "first_manager": "mimi"
}

db.restaurants.insert(r1)

r2 = {
    "name": "casa bonita",
    "address": "Last of the mehicans St 94",
    "first_manager": "tilau"
}

db.restaurants.insert(r2)

i1 = {
    "name": "bread",
    "type": "vegetarian"
}

i2 = {
    "name": "meat",
    "type": "meat"
}

i3 = {
    "name": "fillet",
    "type": "fish"
}

i4 = {
    "name": "eggs",
    "type": "meat"
}

i5 = {
    "name": "beans",
    "type": "vegetarian"
}

db.ingredients.insert(i1)
db.ingredients.insert(i2)
db.ingredients.insert(i3)
db.ingredients.insert(i5)

d1 = {
    "name": "burrito",
    "cost": 2.99,
    "calories": 332,
    "ingredients": [i1["name"], i2["name"], i5["name"]]
}

db.dishes.insert("castelo da mimi", d1)

d2 = {
    "name": "fish takito",
    "cost":  2.65,
    "calories": 156,
    "ingredients": [i1["name"], i3["name"]]
}

db.dishes.insert("castelo da mimi", d2)

d3 = {
    "name": "burgers",
    "cost": 3.54,
    "calories":  619,
    "ingredients": [i1["name"], i2["name"], i4["name"]]
}

db.dishes.insert("casa bonita", d3)

db.ingredients.remove(i5["name"])

db.dishes.add_ingredient("casa bonita", "burgers", i4, new = True)
db.dishes.add_ingredient("casa bonita", "burgers", i5["name"])
db.dishes.remove_ingredient("castelo da mimi", "burrito", i2["name"])

db.dishes.remove("castelo da mimi", d2["name"])

print "\nUsers: "
for user in db.users.get():
    print json.dumps(user, indent=2)
print "\nRestaurants: "
for restaurant in db.restaurants.get():
    print json.dumps(restaurant, indent=2)
print "\nDishes: "
for dish in db.dishes.get():
    print json.dumps(dish, indent=2)

print "\nIngredients: "
for ingredient in db.ingredients.get():
    print json.dumps(ingredient, indent=2)

db.restaurants.remove(r1["name"])
print json.dumps(db.restaurants.get(), indent=2)

db.users.remove(u1["username"])
print json.dumps(db.users.get(), indent=2)

db.users.remove()
print json.dumps(db.users.get(), indent=2)

db.dishes.remove()
print json.dumps(db.dishes.get(), indent=2)

db.restaurants.remove()
print json.dumps(db.restaurants.get(), indent=2)

db.ingredients.remove()
print json.dumps(db.ingredients.get(), indent=2)

session.close()
os.remove("../sqlite/sqlite.db")
