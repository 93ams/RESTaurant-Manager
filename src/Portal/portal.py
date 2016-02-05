import logging
import mimetypes
import os
import uuid
import webapp2
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from templates import template

static_dir = os.path.join(os.path.dirname(__file__), "static")

# with open('config.json') as d:
# 	config = json.load(d)

#substituir pela base de dados

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



########## Static Files ############

class StaticFilesHandler(webapp2.RequestHandler):
    def get(self, path):
        try:
            f_path = os.path.join(static_dir, path)
            with open(f_path) as f:
                content_type = mimetypes.guess_type(f_path)[0]
                self.response.headers.add_header('Content-Type', content_type)
                self.response.write(f.read())
        except Exception as e:
            print "Static Files"
            print e

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        try:
            self.session_store = sessions.get_store(request=self.request)
        except Exception as e:
            print "Dispatch"
            print e
        try:
            response = super(BaseHandler, self).dispatch()
        finally:
			self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session_store(self):
        try:
            store = sessions.get_store(request=self.request)
            return store
        except Exception as e:
            print "Session_store"
            print e

    @webapp2.cached_property
    def session(self):
        try:
            session = self.session_store.get_session()
            return session
        except Exception as e:
            print "Session"
            print e

    @webapp2.cached_property
    def auth_config(self):
		return {
			'login_url': self.uri_for('login'),
			'logout_url': self.uri_for('logout')
		}

############ Main Handlers ###########

class IndexHandler(BaseHandler):
    def get(self):

        if hasattr(self, "session"):
            session = self.session
            user = session.get('user', None)
            context_dict = {}
            if user:
                context_dict["user"] = user
            self.response.write(template("index.html", context_dict))
        else:
            print "Index GET"

class LogoutHandler(BaseHandler):
    def post(self):
        try:
            if hasattr(self, "session"):
                session = self.session
                user = session.get("user", None)
                if user:
                    del self.session["user"]
            else:
                print "Logout"
        except Exception as e:
            print e
            print "Logout"
        self.redirect("/")

class LoginHandler(BaseHandler):
    def get(self):
        try:
            if hasattr(self, "session"):
                session = self.session
                if session.get("user", None):
                    self.redirect("/")
                else:
                    context_dict = {"register": True}
                    self.response.write(template("login.html", context_dict))
            else:
                print "Login GET"
        except Exception as e:
            print "Login GET"
            print e

    def post(self):
        try:
            if self.request.POST.get("register", None):
                self.redirect("/register")
            elif self.request.POST.get("login", None): #depois logo me preocupo com a seguranca
                if hasattr(self, "session"):
                    session = self.session
                    user = session.get("user", None)
                    if user:
                        self.redirect("/")
                    else:
                        username = str(self.request.POST.get("username", None))
                        password = str(self.request.POST.get("password", None))
                        if username:
                            user = users.get(username, None)
                            if password:
                                if user:
                                    if user == password:
                                        self.session["user"] = username
                                        self.redirect("/")
                                    else:
                                        context_dict = {"register": True,
                                                        "username": username,
                                                        "error": "Invalid Password"}
                                        self.response.write(template("login.html", context_dict))
                                else:
                                    context_dict = {"register": True,
                                                    "username": username,
                                                    "error": "Invalid Username"}
                                    self.response.write(template("login.html", context_dict))
                            else:
                                context_dict = {"register": True,
                                                "error": "Please insert a password"}
                                self.response.write(template("login.html", context_dict))
                        else:
                            context_dict = {"register": True,
                                            "error": "Please insert username"}
                            self.response.write(template("login.html", context_dict))
                else:
                    print "Login PUT"
            else:
                self.redirect("/")

        except (InvalidAuthIdError, InvalidPasswordError), e:
            print "Login POST"
            print e

class RegisterHandler(BaseHandler):
    def get(self):
        try:
            if hasattr(self, "session"):
                session = self.session
                user = session.get("user", None)
                if user:
                    self.redirect("/")
                else:
                    context_dict = {"register": True}
                    self.response.write(template("register.html", context_dict))
            else:
                print "Register GET"
        except Exception as e:
            print "Register GET"
            print e

    def post(self):
        try:
            if hasattr(self, "session"):
                username = self.request.POST.get("username", None)
                password = self.request.POST.get("password", None)

                if username:
                    user = users.get(str(username), None)
                    if password:
                        if user:
                            context_dict = {"register": True,
                                            "error": "user already exists"}
                            self.response.write(template("register.html", context_dict))
                        else:
                            if hasattr(self, "session"):
                                self.session["user"] = username
                                users[username] = password
                            else:
                                print "Register POST"
                                print "no session"
                            self.redirect("/")
                    else:
                        context_dict = {"register": True,
                                        "error": "please insert a password"}
                        self.response.write(template("register.html", context_dict))
                else:
                    print "Register POST"
                    context_dict = {"register": True,
                                    "error": "please insert a username and a password"}
                    self.response.write(template("register.html", context_dict))
        except (InvalidAuthIdError, InvalidPasswordError), e:
            print "Register POST"
            print e
            self.redirect("/")

############# Http Handlers ##########

class RestaurantHttpHandler(BaseHandler):
    def get(self, RestaurantName = None, RestaurantID = None):
        if hasattr(self, "session"):
            user = self.session.get("user", None)
            context_dict = {}
            if user:
                context_dict["user"] = user
            context_dict["restaurants"] = restaurants
            self.response.write(template("restaurants.html", context_dict))

        else:
            print "Restaurant Http GET"

class NewRestaurantHandler(BaseHandler):
    def get(self, RestaurantName = None, RestaurantID = None):
        if hasattr(self, "session"):
            user = self.session.get("user", None)
            context_dict = {}
            if user:
                context_dict["user"] = user
            self.response.write(template("new_restaurant.html", context_dict))

        else:
            print "NewRestaurant GET"

    def post(self):
        try:
            if hasattr(self, "session"):
                session = self.session
                user = self.session.get("user", None)
                context_dict = {}
                if user:
                    context_dict["user"] = user
                    name = self.request.POST.get("name", None)
                    address = self.request.POST.get("address", None)
                    if name:
                        if address:
                            new_restaurant = {}
                            new_restaurant["name"] = name
                            new_restaurant["address"] = address
                            id = uuid.uuid4()
                            restaurants[id] = new_restaurant
                            self.redirect("/html/restaurants")
                        else:
                            context_dict["error"] = "Please insert an address"
                            self.response.write(template("new_restaurant.html", context_dict))
                    else:
                        if address:
                            context_dict["error"] = "Please insert a name"
                            self.response.write(template("new_restaurant.html", context_dict))
                        else:
                            context_dict["error"] = "Please insert a name and an address"
                            self.response.write(template("new_restaurant.html", context_dict))

                else:
                    context_dict["error"] = "you have to be loged in to add a new restaurant"
                    self.response.write(template("new_restaurant.html", context_dict))
            else:
                print "Login GET"
        except Exception as e:
            print "Login GET"
            print e

############# Json Handlers ##########

class RestaurantJsonHandler(BaseHandler):
    def get(self, RestaurantName = None, RestaurantID = None):
        if hasattr(self, "session"):
            user = self.session.get("user", None)
            if user:
                pass
            else:
                pass
        else:
            print "Restaurant Json GET"

    def post(self):
        if hasattr(self, "session"):
            user = self.session.get("user", None)
            if user:
                pass
            else:
                pass
        else:
            print "Restaurant Json POST"

    def put(self, RestaurantID = None):
        if hasattr(self, "session"):
            user = self.session.get("user", None)
            if user:
                pass
            else:
                pass
        else:
            print "Restaurant Json PUT"

    def delete(self, RestaurantID = None):
        if hasattr(self, "session"):
            user = self.session.get("user", None)
            if user:
                pass
            else:
                pass
        else:
            print "Restaurant Json DELETE"


############## Routes ###############

routes = [
    # Static Files route
    webapp2.Route(r'/static/<path:[\w/.-]+>', StaticFilesHandler, name="static"),

    # Main Routes
    webapp2.Route(r'/', IndexHandler, name="index"),
    webapp2.Route(r'/login', LoginHandler, name="login"),
    webapp2.Route(r'/logout', LogoutHandler, name="logout"),
    webapp2.Route(r'/register', RegisterHandler, name="register"),

    # Http Routes
    webapp2.Route(r'/html/restaurants', RestaurantHttpHandler, name="restaurants-http"),
    webapp2.Route(r'/html/new_restaurant', NewRestaurantHandler, name="new-restaurant"),
    webapp2.Route(r'/html/restaurants/by_name/<ResturantName:\w+>', RestaurantHttpHandler, name="retaurants-name-http"),
    webapp2.Route(r'/html/restaurants/<ResturantID:[\w-]+>', RestaurantHttpHandler, name="retaurant-http"),

    # Json Routes
    webapp2.Route(r'/json/restaurants', RestaurantJsonHandler, name="retaurants-json"),
    webapp2.Route(r'/json/restaurants/by_name/<ResturantName:\w+>', RestaurantJsonHandler, name="retaurants-name-json"),
    webapp2.Route(r'/json/restaurants/<ResturantID:[\w-]+>', RestaurantJsonHandler, name="retaurant-json"),
]

############### config ###############

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'something-very-very-secret',
}

############### app #################

app = webapp2.WSGIApplication(routes=routes, debug=True, config=config)

########## error Handlers ############

app.error_handlers[404] = handle_404
app.error_handlers[405] = handle_405
app.error_handlers[500] = handle_500

################ main ################

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8000')

############ direct call #############

if __name__ == "__main__":
    #test
    main()
