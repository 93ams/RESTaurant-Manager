from ming import Session, create_datastore
from ming import Document, Field, schema

class User(Document):
     class __mongometa__:
        session = session
        name = 'user'

    _id = Field(schema.ObjectId)
    username = Field(str)
    password = Field(str)

class Restaurant(Document):
     class __mongometa__:
        session = session
        name = 'restaurant'

    _id = Field(schema.ObjectId)
    name = Field(str)
    address = Field(str)

class Users(object):
    def __init__(self, db):
        self.__collection = db.users

    def get(self, username = None):
        try:
            if username:
                pass
            else:
                pass
        except:
            if username:
                return {}
            else:
                return []

    def insert(self, uid = None, username, password):
        try:
            user = User(_id = uid, username = username, password = password)
            return True
        except:
            return False

    def update(self, Username):
        try:
            return True
        except:
            return False

    def remove(self, Username = None):
        try:
            if Username:
                pass
            else:
                pass
            return True
        except:
            return False

class Restaurants(object):
    def __init__(self, db):
        self.__collection = db.restaurants

    def get(self):
        try:
            pass
        except:
            return {}

    def insert(self, name, address):
        try:
            restaurant = Restaurant(name = name, address = address)
            return True
        except:
            return False

    def update(self):
        try:
            return True
        except:
            return False

    def remove(self, RestaurantID = None):
        try:
            if RestaurantID:
                pass
            else:
                pass
            return True
        except:
            return False

class Database(object):
    def __init__(self):
        bind = create_datastore('mongodb://localhost:27017/RESTaurant_Manager')
        self.__db = Session(bind)
        self.restaurants = Restaurants(self.__db)
        self.users = Users(self.__db)

def main():
    db = Database()

if __name__ == "__main__":
    #test
    main()
