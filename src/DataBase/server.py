import webapp2
import json
from database import Database

methods = {
            "Help": "/help",
            "Users": "/users",
            "Restaurants": "/restaurants",
            "Dishes": "/dishes",
            "Ingredients": "/ingredients"
        }

db = Database()

###### error handlers ##############

def handle_404(request, response, exception):
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)

def handle_405(request, response, exception):
    response.write('Malandro!')
    response.set_status(405)

def handle_500(request, response, exception):
    print exception
    response.write('A server error occurred!')
    response.set_status(500)

######## main handlers ###########

class Index(webapp2.RequestHandler):
    def get(self):
        self.redirect("/help")

class Help(webapp2.RequestHandler):
    def get(self):
        try:
            self.response.write(json.dumps(methods))
        except:
            self.response.write(json.dumps({}))

class Users(webapp2.RequestHandler):
    def get(self, username = None):
        try:
            if username:
                user = db.users.get(username = username)
                self.response.write(json.dumps(user))
            else:
                users = db.users.get()
                self.response.write(json.dumps(users))
        except Exception as e:
            print "Users GET"
            print e
            if username:
                self.response.write(json.dumps({}))
            else:
                self.response.write(json.dumps([]))

    def post(self):
        try:
            username = self.request.POST.get("username", None)
            name = self.request.POST.get("name", None)
            password = self.request.POST.get("password", None)
            if not (username or password or name):
                content = json.loads(self.request.body)
                username = content.get("username", None)
                name = content.get("name", None)
                password = content.get("password", None)
            if username and password and name:
                u =  db.users.get(username = username)
                if not u:
                    new_user = {"username": username,
                                "name": name,
                                "password": password}
                    if db.users.insert(new_user):
                        self.response.write("OK")
                    else:
                        self.response.write("FAIL")
                else:
                    self.response.write("FAIL")
            else:
                self.response.write("FAIL")
        except Exception as e:
            print "Users POST"
            print e
            self.response.write("FAIL")

    def put(self, username):
        try:
            content = json.loads(self.request.body)
            data["password"] = content.get("password", None)
            if db.users.update(username, data):
                self.response.write("OK")
            else:
                self.response.write("FAIL")
        except Exception as e:
            print "Users PUT"
            print e
            self.response.write("FAIL")

    def delete(self, username = None):
        try:
            if username:
                if db.users.remove(username):
                    self.response.write("OK")
                else:
                    self.response.write("FAIL")
            else:
                if db.users.remove():
                    self.response.write("OK")
                else:
                    self.response.write("FAIL")
        except  Exception as e:
            print "Users DELETE"
            print e
            self.response.write("FAIL")

class Restaurants(webapp2.RequestHandler):
    def get(self, name = None):
        try:
            if name:
                restaurants = db.restaurants.get(name)
                self.response.write(json.dumps(restaurants))
            else:
                restaurants = db.restaurants.get()
                self.response.write(json.dumps(restaurants))
        except Exception as e:
            print "Restaurants GET"
            print e
            if name:
                self.response.write(json.dumps({}))
            else:
                self.response.write(json.dumps([]))

    def post(self):
        try:
            name = self.request.POST.get("name", None)
            address = self.request.POST.get("address", None)
            manager = self.request.POST.get("first_manager", None)
            if not (name or address):
                content = json.loads(self.request.body)
                name = content.get("name", "")
                address = content.get("address", "")
                manager = content.get("first_manager", "")
            if name and address and manager:
                new_restaurant = {
                    "name": name,
                    "address": address,
                    "first_manager": manager
                }
                if db.restaurants.insert(new_restaurant):
                    self.response.write("OK")
                else:
                    self.response.write("FAIL")
            else:
                self.response.write("FAIL")
        except Exception as e:
            print "Restaurants POST"
            print e
            self.response.write("FAIL")

    def put(self, name):
        try:
            content = json.loads(self.request.body)
            data = {}
            data["address"] = content.get("address", None)
            if db.restaurants.update(name, data):
                self.response.write("OK")
            else:
                self.response.write("FAIL")
        except Exception as e:
            print "Dishes PUT"
            print e
            self.response.write("FAIL")

    def delete(self, name=None):
        try:
            if name:
                if db.restaurants.remove(name):
                    self.response.write("OK")
                else:
                    self.response.write("FAIL")
            else:
                if db.restaurants.remove():
                    self.response.write("OK")
                else:
                    self.response.write("FAIL")
        except Exception as e:
            print "Restaurants DELETE"
            print e
            self.response.write("FAIL")

class Dishes(webapp2.RequestHandler):
    def get(self, name = None, restaurant = None):
        try:
            if restaurant:
                if name:
                    dish = db.dishes.get(restaurant=restaurant, name=name)
                    self.response.write(json.dumps(dish))
                else:
                    dishes = db.dishes.get(restaurant=restaurant)
                    self.response.write(json.dumps(dishes))
            else:
                if name:
                    dishes = db.dishes.get(name=name)
                else:
                    dishes = db.dishes.get()
                self.response.write(json.dumps(dishes))
        except Exception as e:
            print "Dishes GET"
            print e
            if name:
                self.response.write(json.dumps({}))
            else:
                self.response.write(json.dumps([]))

    def post(self, restaurant):
        name = self.request.POST.get("name", None)
        cost = self.request.POST.get("cost", None)
        calories = self.request.POST.get("calories", None)
        if not (name or cost or calories):
            content = json.loads(self.request.body)
            name = content.get("name", "")
            cost = content.get("cost", -1.00)
            calories = content.get("calories", -1)
            ingredients = content.get("ingredients", [])
        if name and cost and calories and restaurant:
            new_dish = {
                "name": name,
                "cost": cost,
                "calories": calories,
                "ingredients": ingredients
            }
            try:
                if db.dishes.insert(restaurant, new_dish):
                    self.response.write("OK")
                else:
                    self.response.write("FAIL")
            except Exception as e:
                print "Dish POST"
                print e
                self.response.write("FAIL")
        else:
            self.response.write("FAIL")

    def put(self):
        try:
            content = json.loads(self.request.body)
            data = {}
            data["cost"] = content.get("cost", None)
            data["calories"] = content.get("calories", None)
            if db.dishes.update(restaurant, name, data):
                self.response.write("OK")
            else:
                self.response.write("FAIL")
        except Exception as e:
            print "Dishes PUT"
            print e
            self.response.write("FAIL")

    def delete(self, name=None, restaurant=None):
        try:
            if restaurant:
                if name:
                    if db.dishes.remove(restaurant=restaurant, name=name):
                        self.response.write("OK")
                    else:
                        self.response.write("FAIL")
                else:
                    if db.dishes.remove(restaurant=restaurant):
                        self.response.write("OK")
                    else:
                        self.response.write("FAIL")
            else:
                if name:
                    if db.dishes.remove(name=name):
                        self.response.write("OK")
                    else:
                        self.response.write("FAIL")
                else:
                    if db.dishes.remove():
                        self.response.write("OK")
                    else:
                        self.response.write("FAIL")
        except Exception as e:
            print "Dishes DELETE"
            print e
            self.response.write("FAIL")

class Ingredients(webapp2.RequestHandler):
    def get(self, name = None, restaurant = None, dish = None):
        try:
            if name:
                ingredient = db.ingredients.get(name=name)
                self.response.write(json.dumps(ingredient))
            else:
                if restaurant:
                    if dish:
                        ingredients = db.ingredients.get(restaurant=restaurant, dish=dish)
                    else:
                        ingredients = db.ingredients.get(restaurant=restaurant)
                else:
                    ingredients = db.ingredients.get()
                self.response.write(json.dumps(ingredients))
        except Exception as e:
            print "Ingredients GET"
            print e
            if name:
                self.response.write(json.dumps({}))
            else:
                self.response.write(json.dumps([]))

    def post(self):
        name = self.request.POST.get("name", None)
        type = self.request.POST.get("type", None)
        if not (name or type):
            content = json.loads(self.request.body)
            name = content.get("name", "")
            type = content.get("type", "")
        if name and (type in ["meat", "fish", "vegetarian"]):
            new_ingredient = {
                "name": name,
                "type": type
            }
            if db.ingredients.insert(new_ingredient):
                self.response.write("OK")
            else:
                self.response.write("FAIL")
        else:
            self.response.write("FAIL")

    def put(self, name):
        try:
            content = json.loads(self.request.body)
            type = content.get("type", "")
            if type:
                if type in ["meat", "fish", "vegetarian"]:
                    if db.dishes.update(name, data):
                        self.response.write("OK")
                    else:
                        self.response.write("FAIL")
                else:
                    self.response.write("FAIL")
            else:
                self.response.write("OK")
        except Exception as e:
            print "Dishes PUT"
            print e
            self.response.write("FAIL")

    def delete(self, name=None, restaurant=None, dish=None):
        try:
            if name:
                if db.ingredients.remove(name=name):
                    self.response.write("OK")
                else:
                    self.response.write("FAIL")
            else:
                if restaurant:
                    if dish:
                        if db.ingredients.remove(restaurant=restaurant, name=dish):
                            self.response.write("OK")
                        else:
                            self.response.write("FAIL")
                    else:
                        self.response.write("FAIL")
                else:
                    if db.ingredients.remove():
                        self.response.write("OK")
                    else:
                        self.response.write("FAIL")
        except Exception as e:
            print "Ingredient Delete"

routes = [
    webapp2.Route(r'/', Index),
    webapp2.Route(r'/help', Help),

    webapp2.Route(r'/users', Users),
    webapp2.Route(r'/users/<username>', Users),

    webapp2.Route(r'/restaurants', Restaurants),
    webapp2.Route(r'/restaurants/<name>', Restaurants),

    webapp2.Route(r'/dishes', Dishes),
    webapp2.Route(r'/dishes/<name>', Dishes),
    webapp2.Route(r'/restaurants/<restaurant>/dishes', Dishes),
    webapp2.Route(r'/restaurants/<restaurant>/dishes/<name>', Dishes),

    webapp2.Route(r'/ingredients', Ingredients),
    webapp2.Route(r'/ingredients/<name>', Ingredients),
    webapp2.Route(r'/restaurants/<restaurant>/dishes/<dish>/ingredients', Ingredients)
]

config = {}
config['webapp2_extras.sessions'] = {
     'secret_key': 'something-very-very-secret',
}

app = webapp2.WSGIApplication(routes=routes, debug=True, config=config)

########## error Handlers ############

app.error_handlers[404] = handle_404
app.error_handlers[405] = handle_405
app.error_handlers[500] = handle_500

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='7000')

if __name__ == "__main__":
    #test
    main()
