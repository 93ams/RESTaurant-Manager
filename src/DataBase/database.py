#!/usr/bin/env python
from DbClasses import User, Restaurant, Dish, Ingredient, session
from load_database import load
from ming.odm import Mapper
Mapper.compile_all()

def serializer(type, obj, multi=False):
    try:
        if type == "user":
            if multi:
                user_list = []
                for o in obj:
                    user_list.append({
                        "username": str(o.username),
                        "password": str(o.password)
                    })
                return user_list
            else:
                user = {}
                if obj:
                    user["username"] = str(obj.username)
                    user["password"] =  str(obj.password)
                return user
        elif type == "restaurant":
            if multi:
                restaurant_list = []
                for o in obj:
                    restaurant_list.append({
                        "RestaurantID": str(o.restaurant_id),
                        "Name": str(o.name),
                        "Address": str(o.address)
                    })
                return restaurant_list
            else:
                restaurant = {}
                if obj:
                    restaurant["RestaurantID"] = str(obj.restaurant_id)
                    restaurant["Name"] = str(obj.name)
                    restaurant["Address"] = str(obj.address)
                return restaurant
        elif type == "dish":
            if multi:
                dish_list = []
                for o in obj:
                    dish_list.append({
                        "Name": str(o.name),
                        "Rate": float(o.rate),
                        "Cost": float(o.cost),
                        "Calories": int(o.calories)
                    })
                return dish_list
            else:
                dish = {}
                if obj:
                    dish = {
                        "Name": str(obj.name),
                        "Rate": float(obj.rate),
                        "Cost": float(obj.cost),
                        "Calories": int(obj.calories)
                    }
                return dish
        elif type == "ingredient":
            if multi:
                ingredient_list = []
                for o in obj:
                    ingredient_list.append({
                        "Name": str(o.name),
                        "Type": str(o.type),
                        "Allergens": o.allergens,
                        "Description": str(o.description)
                    })
                return ingredient_list
            else:
                ingredient = {}
                if obj:
                    ingredient = {
                        "Name": str(obj.name),
                        "Type": str(obj.type),
                        "Allergens": obj.allergens,
                        "Description": str(obj.description)
                    }
                return ingredient

    except Exception as e:
        print "Serializer"
        print e
        if multi:
            return []
        else:
            return {}

class Users(object):
    def get(self, username = None):
        try:
            if username:
                user = User.query.get(username = username)
                return serializer("user", user)
            else:
                users = User.query.find({})
                return serializer("user", users, multi=True)
        except Exception as e:
            print "Users Get"
            print e
            if username:
                return {}
            else:
                return []

    def insert(self, user):
        try:
            username = user.get("username", "")
            password = user.get("password", "")
            fid = user.get("fid", "")
            if username and password:
                User(username = username, password = password, fid = fid, manager=False)
                session.flush()
            return True
        except Exception as e:
            print e
            return False

    def update(self, Username, password = None):
        try:
            user = User.query.get(username = Username)
            if password:
                user.password = password
            session.flush()
            return True
        except Exception as e:
            print e
            return False

    def remove(self, username = None):
        try:
            if username:
                user = User.query.get(username = username)
                user.delete()
            else:
                users = User.query.find({})
                for user in users:
                    user.delete()
            session.flush()
            return True
        except Exception as e:
            print e
            return False

class Restaurants(object):
    def get(self, RestaurantID = None, RestaurantName = None):
        try:
            if RestaurantID:
                restaurant = Restaurant.query.get(restaurant_id = RestaurantID)
                return serializer("restaurant", restaurant)
            elif RestaurantName:
                restaurants = Restaurant.query.find(name = RestaurantName)
                return serializer("restaurant", restaurants, multi=True)
            else:
                restaurants = Restaurant.query.find({})
                return serializer("restaurant", restaurants, multi=True)

        except Exception as e:
            print e
            if RestaurantID:
                return {}
            else:
                return []

    def insert(self, restaurant):
        try:
            id = restaurant.get("restaurant_id", "")
            name = restaurant.get("name", "")
            address = restaurant.get("address", "")
            if id and name and address:
                Restaurant(restaurant_id = id, name = name, address = address)
                session.flush()
            return True
        except Exception as e:
            print e
            return False

    def update(self, RestaurantID, name = None, address = None):
        try:
            restaurant = Restaurant.query.get(restaurant_id = RestaurantID)
            if name:
                restaurant.name = name
            if address:
                restaurant.address = address
            session.flush()
            return True
        except Exception as e:
            print e
            return False

    def remove(self, RestaurantID = None):
        try:
            if RestaurantID:
                restaurant = Restaurant.query.get(_id = RestaurantID)
                restaurant.delete()
            else:
                restaurants = Restaurant.query.find({})
                for restaurant in restaurants:
                    restaurant.delete()
            session.flush()
            return True
        except Exception as e:
            print e
            return False

class Dishes(object):
    def get(self, RestaurantID=None, Name=None):
        try:
            if RestaurantID:
                restaurant = Restaurant.query.get(restaurant_id = RestaurantID)
                dishes = restaurant.dishes
                if restaurant:
                    if Name:
                        dish = dishes.query.get(name = Name)
                        return serializer("dish", dish)
                    else:
                        dishes = dishes.query.find()
                        return serializer("dish", dishes, multi=True)
                else:
                    if Name:
                        return {}
                    else:
                        return []
            else:
                if Name:
                    dishes = Dish.query.get(name = Name)
                else:
                    dishes = Dish.query.find()

                dishes = serializer("dish", dishes, multi=True)
                return dishes

        except Exception as e:
            print "Dishes Get"
            print e
            if RestaurantID and Name:
                return {}
            else:
                return []

    def insert(self, dish):
        try:
            RestaurantID = dish.get("restaurant", None)
            if RestaurantID:
                new_ingredients = []
                restaurant = Restaurant.query.get(restaurant_id = RestaurantID)
                if restaurant:
                    name = dish.get("name", None)
                    cost = dish.get("cost", -1.0)
                    calories = dish.get("calories", -1)
                    new_dish = Dish(restaurant=restaurant, name=name, rate=-1, cost=cost, calories=calories)
                    ingredients = dish.get("ingredients", [])
                    for ingredient in ingredients:
                        name =  ingredient.get("name", None)
                        if name:
                            i = Ingredient.query.get(name = ingredient)
                            if not i:
                                type=ingredient.get("type", "")
                                allergens=ingredient.get("allergens", [])
                                description=ingredient.get("description", "")
                                if type:
                                    try:
                                        ["meat", "fish", "vegetarian"].index(type)
                                        i = Ingredient(name=name, type=str(type), allergens=allergens, description=description)
                                    except Exception as e:
                                        print "Dishes Insert"
                                        print e
                                        return False
                            new_ingredients.append(i)
                    new_dish.ingredients = new_ingredients
                    session.flush()
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print "Dishes Insert"
            print e
            return False

    def update(self):
        pass

    def remove(self, RestaurantID = None, DishName = None):
        try:
            if RestaurantID:
                restaurant = Restaurant.query.get(restaurant_id = RestaurantID)
                if restaurant:
                    dishes = restaurant.dishes
                    if DishName:
                        dish = dishes.query.get(name = DishName)
                        if dish:
                            dish.delete()
                        else:
                            return False
                    else:
                        for dish in dishes:
                            dish.delete()
            else:
                dishes = Dish.query.find()
                for dish in dishes:
                    dish.delete()
            session.flush()
            return True
        except Exception as e:
            print "Dish Remove"
            print e
            return False

class Ingredients(object):
    def get(self, name=None, RestaurantID=None, Dish=None, type=None):
        if name:
            ingredient = Ingredient.query.get(name = name)
        else:
            if RestaurantID:
                restaurant = Restaurant.query.get(restaurant_id = RestaurantID)
                if restaurant:
                    dishes = restaurant.dishes
                    if Dish:
                        dish = dishes.query.get(name = Dish)
                        ingredients = dish.ingredients
                        return serializer("ingredient", ingredients, multi=True)
                    else:
                        dishes = dishes.query.find()
                        ingredient_list = []
                        for dish in dishes:
                            ingredient_list.extend(dish.ingredients)
                        print ingredient_list
                        return serializer("ingredient", ingredient_list, multi=True)
            else:
                ingredients = Ingredient.query.find()
                return serializer("ingredient", ingredients, multi=True)

    def insert(self, ingredient):
        try:
            name = ingredient.get("name", None)
            t = ingredient.get("type", None)
            allergens = ingredient.get("allergens", [])
            description = ingredient.get("description", "")
            if (t == "meat" or t == "fish" or t == "vegetarian") and name:
                Ingredient(name = name, type = t, allergens = allergens, description=description)
                session.flush()
                return True
            return False
        except Exception as e:
            print "Ingredients Insert"
            print "aqui"
            print e
            return False

    def update(self):
        pass

    def remove(self, ingredient_name=None):
        try:
            if ingredient_name:
                ingredient = Ingredient.query.get(name=ingredient_name)
                if ingredient:
                    ingredient.delete()
                else:
                    return False
            else:
                ingredients = Ingredient.query.find()
                for ingredient in ingredients:
                    ingredient.delete()
            session.flush()
            return True
        except Exception as e:
            print "Ingredient Remove"
            print e
            return False

class Database(object):
    def __init__(self):
        self.restaurants = Restaurants()
        self.users = Users()
        self.dishes = Dishes()
        self.ingredients = Ingredients()
