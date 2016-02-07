import webapp2
import json
import logging
import uuid
from database import Database

methods = {
            "Help": "/help",
            "Users": "/users",
            "Restaurants": "/restaurants"
        }

db = Database()

###### error handlers ##############

def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)

def handle_405(request, response, exception):
    logging.exception(exception)
    response.write('Malandro!')
    response.set_status(405)

def handle_500(request, response, exception):
    logging.exception(exception)
    response.write('A server error occurred!')
    response.set_status(500)

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
    def get(self, Username = None):
        try:
            if Username:
                user = db.users.get(Username)
                self.response.write(json.dumps(user))
            else:
                users = db.users.get()
                self.response.write(json.dumps(users))
        except Exception as e:
            print "User GET"
            print e
            if Username:
                self.response.write(json.dumps({}))
            else:
                self.response.write(json.dumps([]))

    def post(self):
        try:
            username = self.request.POST.get("Username", None)
            password = self.request.POST.get("Password", None)
            if not (username or password):
                content = json.loads(self.request.body)
                username = content.get("Username", None)
                password = content.get("Password", None)

            if username and password:
                if not db.users.get(username):
                    if db.users.insert(username, password):
                        self.response.write("OK")
                    else:
                        self.response.write("FAIL")
                else:
                    self.response.write("FAIL")
            else:
                self.response.write("FAIL")
        except Exception as e:
            print "User POST"
            print e
            self.response.write("FAIL")

    def put(self, Username):
        try:
            content = json.loads(self.request.body)
            password = content.get("password", None)
            if password:
                pass
            self.response.write("OK")
        except Exception as e:
            print "User PUT"
            print e
            self.response.write("FAIL")

    def delete(self, Username = None):
        try:
            if Username:
                if users.get(Username, None):
                    if db.users.delete(Username):
                        self.response.write("OK")
                    else:
                        self.response.write("FAIL")
                else:
                    self.response.write("FAIL")
            else:
                users = {}
        except  Exception as e:
            print "User DELETE"
            print e
            self.response.write("FAIL")

class Restaurants(webapp2.RequestHandler):
    def get(self, RestaurantName = None, RestaurantID = None):
        try:
            if RestaurantID:
                restaurant = db.restaurants.get(RestaurantID = RestaurantID)
                self.response.write(json.dumps(restaurant))
            elif RestaurantName:
                restaurants = db.restaurants.get(RestaurantName = RestaurantName)
                self.response.write(json.dumps(restaurants))
            else:
                restaurants = db.restaurants.get()
                self.response.write(json.dumps(restaurants))
        except Exception as e:
            print "Restaurants GET"
            print e
            if RestaurantID:
                self.response.write(json.dumps({}))
            else:
                self.response.write(json.dumps([]))

    def post(self):
        try:
            name = self.request.POST.get("Name", None)
            address = self.request.POST.get("Address", None)
            if not (name or address):
                content = json.loads(self.request.body)
                name = content.get("Name", None)
                address = content.get("Address", None)

            if name and address:
                id = str(uuid.uuid4())
                if db.restaurants.insert(id, name, address):
                    self.response.write("OK")
                else:
                    self.response.write("FAIL")
            else:
                self.response.write("FAIL")
        except Exception as e:
            print "Restaurants POST"
            print e
            self.response.write("FAIL")

    def put(self, RestaurantID):
        try:
            content = json.loads(self.request.body)
            name = content.get("name", None)
            address = content.get("address", None)

            if name:
                pass

            if address:
                pass

            self.response.write("OK")
        except Exception as e:
            print "Restaurants PUT"
            print e
            self.response.write("FAIL")

    def delete(self, RestaurantID = None):
        try:
            if ResturantID:
                if restaurants.get(RestaurantID, None):
                    if db.restaurants.delete(ResturantID):
                        self.response.write("OK")
                    else:
                        self.response.write("FAIL")
                else:
                    self.response.write("FAIL")
            else:
                restaurants = {}
                print db.restaurants.delete()
                self.response.write("OK")

        except Exception as e:
            print "Restaurants DELETE"
            print e
            self.response.write("FAIL")

class Dishes(webapp2.RequestHandler):
    def get(self, Name = None, RestaurantID = None):
        pass

    def post(self):
        name = self.request.POST.get("Name", None)
        
        if not (name or address):
            content = json.loads(self.request.body)
            name = content.get("Name", None)

    def put(self):
        pass

    def delete(self):
        pass

class Ingredients(webapp2.RequestHandler):
    def get(self, Name = None, RestaurantID = None, Dish = None):
        pass

    def post(self):
        name = self.request.POST.get("Name", None)

        if not (name or address):
            content = json.loads(self.request.body)
            name = content.get("Name", None)

    def put(self):
        pass

    def delete(self):
        pass

routes = [
    webapp2.Route(r'/', Index),
    webapp2.Route(r'/help', Help),

    webapp2.Route(r'/users', Users),
    webapp2.Route(r'/users/<Username>', Users),

    webapp2.Route(r'/restaurants', Restaurants),
    webapp2.Route(r'/restaurants/<RestaurantID>', Restaurants),
    webapp2.Route(r'/restaurants/search/<RestaurantName>', Restaurants),

    webapp2.Route(r'/dishes', Dishes),
    webapp2.Route(r'/dishes/<Name>', Dishes),
    webapp2.Route(r'/restaurants/<RestaurantID>/dishes', Dishes),
    webapp2.Route(r'/restaurants/<RestaurantID>/dishes/<Name>', Dishes),

    webapp2.Route(r'/ingredients', Ingredients),
    webapp2.Route(r'/ingredients/<Name>', Ingredients),
    webapp2.Route(r'/restaurants/<RestaurantID>/ingredients', Ingredients),
    webapp2.Route(r'/restaurants/<RestaurantID>/dishes/<Dish>/ingredients', Ingredients),
    webapp2.Route(r'/restaurants/<RestaurantID>/dishes/<Dish>/ingredients/<Name>', Ingredients),
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
