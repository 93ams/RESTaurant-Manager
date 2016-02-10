from models import User, Restaurant, Dish, Ingredient
from models import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

DEBUG = True

class Users(object):
    def get(self, username = None):
        try:
            if username:
                data = {}
                u = session.query(User).\
                            filter(User.username == username).\
                            one_or_none()
                if u:
                    data = u.json()
            else:
                data = []
                u = session.query(User).all()
                for user in u:
                    data.append(user.json())
        except Exception as e:
            if DEBUG:
                print "Users Get"
                print e
        session.commit()
        return data

    def insert(self, user): #por opcao para inserir varios de seguida
        if user:
            username = user.get("username", "")
            name = user.get("name", "")
            password = user.get("password", "")
            if username and name and password:
                try:
                    u = User(username = username, name = name, password = password)
                    session.add(u)
                    session.commit()
                    return True
                except Exception as e:
                    if DEBUG:
                        print "Users Insert"
                        print e
                    session.commit()
        return False

    def update(self, username, data):
        try:
            u = session.query(User).filter(User.username == username).one_or_none()
            if u:
                name = data.get("name", "")
                password = data.get("password", "")
                if name:
                    u.name = name
                if password:
                    u.password = password
                session.commit()
                return True
        except Exception as e:
            if DEBUG:
                print "Users Update"
                print e
        session.commit()
        return False

    def remove(self, username=None): #remover varios
        try:
            if username:
                u = session.query(User).filter(User.username == username).one_or_none()
                if u:
                    session.delete(u)
                else:
                    return False
            else:
                u = session.query(User).all()
                for user in u:
                    session.delete(user)
            session.commit()
            return True
        except Exception as e:
            if DEBUG:
                print "Users Remove"
                print e
        session.commit()
        return False

class Restaurants(object):
    def get(self, name = None):
        try:
            if name:
                data = {}
                r = session.query(Restaurant).\
                            filter(Restaurant.name == name).\
                            one_or_none()
                if r:
                    data = r.json()
            else:
                data = []
                r = session.query(Restaurant).all()
                for restaurant in r:
                    data.append(restaurant.json())
        except Exception as e:
            if DEBUG:
                print "Restaurants Get"
                print e
        session.commit()
        return data

    def insert(self, restaurant):
        if restaurant:
            name = restaurant.get("name", "")
            address = restaurant.get("address", "")
            manager = restaurant.get("first_manager", "")
            if name and address and manager :
                try:
                    u = session.query(User).\
                                filter(User.username == manager).\
                                one_or_none()
                    if u:
                        r = Restaurant(name = name, address = address)
                        session.add(r)
                        u.restaurant = r
                        session.commit()
                        return True
                except Exception as e:
                    if DEBUG:
                        print "Restaurants Insert"
                        print e
        session.commit()
        return False

    def update(self, user, data):
        try:
            r = session.query(Restaurant).filter(Restaurant.name == name).one_or_none()
            if r:
                address = data.get("address", "")
                if address:
                    r.address = address
                session.commit()
                return True
        except Exception as e:
            if DEBUG:
                print "Restaurants Update"
                print e
        session.commit()
        return False

    def add_manager(self, restaurant, uses):
        try:
            r = session.query(Restaurant).\
                        filter(Restaurant.name == name).\
                        one_or_none()

            u = session.query(User).\
                        filter(User.username == username).\
                        one_or_none()
            if r and u:
                u.restaurant = r
                session.commit()
                return True

        except Exception as e:
            if DEBUG:
                print "Restaurants Add Manager"
        session.commit()
        return False

    def remove_manager(self, restaurant, uses):
        try:
            r = session.query(Restaurant).\
                        filter(Restaurant.name == name).\
                        one_or_none()

            u = session.query(User).\
                        filter(User.username == username).\
                        one_or_none()
            if r and u and (r in r.managers):
                r.managers.remove(u)
                session.commit()
                return True
        except Exception as e:
            if DEBUG:
                print "Restaurants Remove Manager"
        session.commit()
        return False

    def remove(self, name=None):
        try:
            if name:
                r = session.query(Restaurant, Dishes).\
                            filter(Restaurant.name == name).\
                            join(Dish.restaurant_id == Restaurant.id).\
                            all()

                print r
                if r:
                    r = r[0]
                    print r
                    for dish in r.dishes:
                        session.delete(dish)
                    session.delete(r)
                else:
                    session.commit()
                    return False
            else:
                r = session.query(Restaurant).\
                            all()
                for restaurant in r:
                    d = session.query(Dish).\
                                filter(Dish.restaurant_id == restaurant.id).\
                                all()
                    for dish in d:
                        session.delete(dish)
                    session.delete(restaurant)
            session.commit()
            return True
        except Exception as e:
            if DEBUG:
                print "Restaurant Remove"
                print e
        session.commit()
        return False

class Dishes(object):
    def get(self, restaurant = None, name = None):
        try:
            if restaurant:
                if name:
                    data = {}
                    d = session.query(Restaurant, Dish).\
                                filter(Restaurant.name == restaurant).\
                                join(Restaurant.dishes).\
                                filter(Dish.name == name).\
                                one_or_none()
                    if d:
                        data = d[1].json()
                else:
                    data = []
                    d = session.query(Restaurant, Dish).\
                                filter(Restaurant.name == restaurant).\
                                join(Restaurant.dishes).\
                                all()
                    if d:
                        for dish in d:
                            data.append(dish[1].json())
            else:
                data = []
                if name:
                    d = session.query(Dish).filter(Dish.name == name)
                else:
                    d = session.query(Dish).all()
                for dish in d:
                    data.append(dish.json())
        except Exception as e:
            print "Dishes Get"
            print e
        session.commit()
        return data

    def insert(self, restaurant, dish):
        if restaurant and dish:
            name = dish.get("name", "")
            cost = dish.get("cost", 0.0)
            calories = dish.get("calories", 0)

            if name and cost and calories:
                try:
                    r = session.query(Restaurant).filter(Restaurant.name == restaurant).one_or_none()
                    if r:
                        d = Dish(restaurant_id = r.id, name = name, cost = cost, calories = calories)
                        session.add(d)
                        for i in dish.get("ingredients", []):
                            i = session.query(Ingredient).filter(Ingredient.name == i).one_or_none()
                            if i:
                                d.ingredients.append(i)
                        session.commit()
                        return True
                except Exception as e:
                    print "Dishes Insert"
                    print e
        session.commit()
        return False

    def update(self, restaurant, dish, data):
        try:
            d = session.query(Restaurant, Dish).\
                        filter(Restaurant.name == restaurant).\
                        join(Restaurant.dishes).\
                        filter(Dish.name == dish).\
                        one_or_none()
            if d:
                d = d[1]
                name = data.get("name", "")
                cost = data.get("cost", 0.0)
                calories = data.get("calories", 0)
                if name:
                    d.name = name
                if cost:
                    d.cost = cost
                if calories:
                    d.calories = calories
                session.commit()
                return True
        except Exception as e:
            if DEBUG:
                print "Dishes Update"
                print e
        session.commit()
        return False

    def add_ingredient(self, restaurant, dish, ingredient, new = False):
        if restaurant and dish and ingredient:
            try:
                d = session.query(Restaurant, Dish).\
                            filter(Restaurant.name == restaurant).\
                            join(Restaurant.dishes).\
                            filter(Dish.name == dish).\
                            one_or_none()
                if d:
                    d = d[1]
                    if new:
                        name = ingredient.get("name", "")
                        type = ingredient.get("type", "")

                        if name and (type in ["meat", "fish", "vegetarian"]):
                            i = Ingredient(name = name, type = type)
                            session.add(i)
                        else:
                            print "meh"
                            session.commit()
                            return False
                    else:
                        i = session.query(Ingredient).\
                                    filter(Ingredient.name == ingredient).\
                                    one_or_none()
                        if not i:
                            session.commit()
                            return False
                    d.ingredients.append(i)
                    session.commit()
                    return True
            except Exception as e:
                print "Dishes Add Ingredient"
                print e
                session.commit()
        return False

    def remove_ingredient(self, restaurant, dish, ingredient):
        if restaurant and dish and ingredient:
            try:
                d = session.query(Restaurant, Dish).\
                            filter(Restaurant.name == restaurant).\
                            join(Restaurant.dishes).\
                            filter(Dish.name == dish).\
                            one_or_none()

                if d:
                    d = d[1]
                    i = session.query(Dish, Ingredient).\
                                filter(Dish.restaurant_id == d.restaurant_id).\
                                filter(Dish.name == d.name).\
                                join(Dish.ingredients).\
                                filter(Ingredient.name == ingredient).\
                                one_or_none()
                    if i:
                        i = i[1]
                        d.ingredients.remove(i)
                        session.commit()
                        return True
            except Exception as e:
                print "Dishes Remove Ingredient"
                print e
        session.commit()
        return False

    def remove(self, restaurant=None, name=None):
        try:
            if restaurant:
                if name:
                    d = session.query(Restaurant, Dish).\
                                filter(Restaurant.name == restaurant).\
                                join(Restaurant.dishes).\
                                filter(Dish.name == name).\
                                one_or_none()
                    if d:
                        d = d[1]
                        session.delete(d)
                    else:
                        session.commit()
                        return False
                else:
                    d = session.query(Restaurant, Dish).\
                                filter(Restaurant.name == restaurant).\
                                join(Restaurant.dishes).\
                                all()
                    for dish in d:
                        session.delete(dish[1])
            else:
                d = session.query(Dish).all()
                for dish in d:
                    session.delete(dish)
            session.commit()
            return True
        except Exception as e:
            if DEBUG:
                print "Dish Remove"
                print e
        session.commit()
        return False

class Ingredients(object):
    def get(self, name = None, restaurant = None, dish = None):
        try:
            if name:
                data = {}
                i = session.query(Ingredient).filter(Ingredient.name == name).one_or_none()
                if i:
                    data = i.json()

            else:
                data = []
                if restaurant and dish:
                    d = session.query(Restaurant, Dish).\
                                filter(Restaurant.name == restaurant).\
                                join(Restaurant.dishes).\
                                filter(Dish.name == dish).\
                                one_or_none()

                    if d:
                        d = d[1]
                        for ingredient in d.ingredients:
                            data.append(ingredient.json())
                else:
                    i = session.query(Ingredient).all()
                    for ingredient in i:
                        data.append(ingredient.json())
        except Exception as e:
            print "Ingredients Get"
            print e
        session.commit()
        return data

    def insert(self, ingredient):
        if ingredient:
            name = ingredient.get("name", "")
            type = ingredient.get("type", "")

            if name and (type in ["meat", "fish", "vegetarian"]):
                try:
                    i = Ingredient(name = name, type = type)
                    session.add(i)
                    session.commit()
                    return True
                except Exception as e:
                    print "Ingredient Insert"
                    print e
        session.commit()
        return False

    def update(self, user, data):
        try:
            i = session.query(Ingredient).filter(Ingredient.name == name).one_or_none()
            if i:
                type = data.get("type", "")
                if type in ["meat", "fish", "vegetarian"]:
                    i.type = type
                session.commit()
                return True
        except Exception as e:
            if DEBUG:
                print "Ingredients Update"
                print e
        session.commit()
        return False

    def remove(self, name=None):
        try:
            if name:
                i = session.query(Ingredient).\
                            filter(Ingredient.name == name).\
                            one_or_none()
                if i:
                    session.delete(i)
                else:
                    return False
            else:
                i = session.query(Ingredient).all()
                for ingredient in i:
                    session.delete(ingredient)
            session.commit()
            return True

        except Exception as e:
            if DEBUG:
                print "Ingredients Remove"
                print e

        return False

class Database(object):
    def __init__(self):
        self.users = Users()
        self.restaurants = Restaurants()
        self.dishes = Dishes()
        self.ingredients = Ingredients()
