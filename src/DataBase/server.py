import webapp2
import json
from database import Database as db

methods = {
            "Help": "/help",
            "Users": "/users",
            "Restaurants": "/restaurants"
        }

users = {}
restaurants = {}

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
                self.response.write(json.dumps(users.get(Username, {})))
            else:
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
            print self.request.body
            content = json.loads(self.request.body)
            print content
            username = content.get("username", None)
            password = content.get("password", None)
            if username and password:
                users[username] = password
                self.response.write("OK")
            else:
                self.response.write("FAIL")
        except Exception as e:
            print "User POST"
            print e
            self.response.write("FAIL")

    def put(self, Username):
        try:

            self.response.write("OK")
        except Exception as e:
            print "User PUT"
            print e
            self.response.write("FAIL")

    def delete(self, Username = None):
        try:
            if Username:
                if users.get(Username, None):
                    del users[Username]
                    self.response.write("OK")
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
                self.response.write(json.dumps(restaurants.get(RestaurantID, {})))
            elif RestaurantName:
                restaurant_list = []
                for restaurant in restaurants:
                    if restaurant["name"] == RestaurantName:
                        restaurant_list.append(restaurant)
                self.response.write(json.dumps(restaurants_list))
            else:
                self.response.write(json.dumps(restaurants))
        except:
            if RestaurantID:
                self.response.write(json.dumps({}))
            else:
                self.response.write(json.dumps([]))

    def post(self):
        try:
            content = json.loads(self.request.body())
            name = content.get("name", None)
            address = content.get("address", None)

            if name and address:
                new_restaurant = {}
                new_restaurant["name"] = name
                new_restaurant["address"] = address
                id = uuid.uuid4()
                restaurants[id] = new_restaurant
                self.response.write("OK")
            else:
                self.response.write("FAIL")
        except:
            self.response.write("FAIL")

    def put(self, RestaurantID):
        try:

            self.response.write("OK")
        except:
            self.response.write("FAIL")

    def delete(self, RestaurantID = None):
        try:
            if ResturantID:
                if restaurants.get(RestaurantID, None):
                    self.response.("OK")
                else:
                    self.response.write("FAIL")
            else:
                restaurants = {}
                self.response.("OK")

        except:
            self.response.write("FAIL")

routes = [
    webapp2.Route(r'/', Index),
    webapp2.Route(r'/help', Help),
    webapp2.Route(r'/users', Users),
    webapp2.Route(r'/users/<Username>', Users),
    webapp2.Route(r'/restaurants', Restaurants),
    webapp2.Route(r'/restaurants/<RestaurantID>', Restaurants),
    webapp2.Route(r'/restaurants/<RestaurantName>', Restaurants),
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
