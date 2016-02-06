#!/usr/bin/env python
from ming import create_datastore
from ming.odm import ThreadLocalODMSession

session = ThreadLocalODMSession(
bind = create_datastore('mongodb://localhost:27017/RESTaurant_Manager')
)

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty

class User(MappedClass):
    class __mongometa__:
        session = session
        name = 'user'

    _id = FieldProperty(schema.ObjectId)
    username = FieldProperty(schema.String(required=True))
    password = FieldProperty(schema.String(required=True))

class Restaurant(MappedClass):
    class __mongometa__:
        session = session
        name = 'restaurant'

    _id = FieldProperty(schema.ObjectId)
    restaurant_id = FieldProperty(schema.String(required=True))
    name = FieldProperty(schema.String(required=True))
    address = FieldProperty(schema.String(required=True))

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
    except Exception as e:
        print "Serializer"
        print e

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

    def insert(self, username, password):
        try:
            User(username = username, password = password)
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

    def insert(self, id, name, address):
        try:
            restaurant = Restaurant(restaurant_id = id, name = name, address = address)
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

class Database(object):
    def __init__(self):
        self.restaurants = Restaurants()
        self.users = Users()
