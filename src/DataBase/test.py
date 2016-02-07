from database import Database
from load_database import load
import uuid

def print_commands(detail=False):
    print "Commands: "
    print "G: Get"
    print "I: Insert"
    print "U: Update"
    print "D: Delete"
    print "L: Load"
    print "R: Reset"
    print "M: Menu"
    print "E: Exit"
    if detail:
        print " ----------------------------------------------------------------------------------------------------------------------------- "
        print " | [cmd] | [collection] |                            [arguments]                                  ||       Description       | "
        print " |-------|--------------|-------------------------------------------------------------------------||-------------------------| "
        print " |   G   |      U       | [Username]                                                              || Gets user(s)            | "
        print " |   G   |      R       | [RestaurantID] [Name]                                                   || Gets restaurant(s)      | "
        print " |   G   |      D       | [RestaurantID] [Dish]                                                   || Gets dish(es)           | "
        print " |   G   |      I       | [Ingredient] [Dish]                                                     || Gets ingredient(s)      | "
        print " |   I   |      U       | Username Password FiscalID                                              || Insert a new user       | "
        print " |   I   |      R       | RestaurantID Name Address                                               || Insert a new restaurant | "
        print " |   I   |      D       | Name RestaurantID (List of Ingredients) Calories                        || Insert a new dish       | "
        print " |   I   |      I       | RestaurantID Name Address                                               || Insert a new ingredient | "
        print " |   U   |      U       | Username [Password] [FiscalID]                                          || Updates user            | "
        print " |   U   |      R       | RestaurantID [Name][Address]                                            || Updates restaurant      | "
        print " |   U   |      D       | RestaurantID Dish [(add/remove) ingredient] [price] [rate] [calories]   || Updates dish            | "
        print " |   U   |      I       | Ingredient [type] [(add/remove) allergen] [description]                 || Updates ingredient      | "
        print " |   D   |      U       | [Username]                                                              || Deletes user(s)         | "
        print " |   D   |      R       | [RestaurantID]                                                          || Deletes restaurant(s)   | "
        print " |   D   |      D       | RestaurantID Dish                                                       || Deletes dish(s)         | "
        print " |   D   |      I       | Ingredient                                                              || Deletes ingredient(s)   | "
        print " |   L   |      -       | Filepath                                                                || Loads content from file | "
        print " |   R   |      -       |                                                                         || Resets the database     | "
        print " |   E   |      -       |                                                                         || Exit the program        | "
        print " ----------------------------------------------------------------------------------------------------------------------------- "

def command(db, cmd, col):
    if cmd == "G":
        if col == "U":
            print "insert username for a specific user or don't for all users"
            username = raw_input("Username> ")
            if username:
                return db.users.get(username)
            else:
                return db.users.get()

        elif col == "R":
            print "insert id for a specific restaurant or don't for next option"
            RestaurantID = raw_input("RestaurantID> ")
            if RestaurantID:
                return db.restaurants.get(RestaurantID = RestaurantID)
            else:
                print "insert name for all the restaurants with that name or don't for all restaurants"
                RestaurantName = raw_input("RestaurantName> ")
                if RestaurantName:
                    return db.restaurants.get(RestaurantName = RestaurantName)
                else:
                    choice = raw_input("All Restaurants? [Y/n]")
                    if choice in ["", "Y", "y"]:
                        return db.restaurants.get()

        elif col == "D":
            print "insert restaurant_id for all dishes of that restaurant or don't for next option"
            RestaurantID = raw_input("RestaurantID> ")
            if RestaurantID:
                restaurant = db.restaurants.get(restaurant_id = RestaurantID)
                if restaurant:
                    print "insert dish name for specific dish or don't for all the dishes in the restaurant"
                    DishName = raw_input("DishName> ")
                    if DishName:
                        return db.dish.get(restaurant_id = RestaurantID, name = DishName)
                    else:
                        return db.dish.get(restaurant_id = RestaurantID)
                else:
                    print "restaurant doesn't exist yet"
                    return
            else:
                print "insert Dish name for all dishes with that name or don't for all dishes"
                DishName = raw_input("DishName> ")
                if DishName:
                    return db.dishes.get(name = DishName)
                else:
                    choice = raw_input("All Dishes? [Y/n]")
                    if choice in ["", "Y", "y"]:
                        print "getting all dishes"
                        return db.dishes.get()
                    else:
                        return []

        elif col == "I":
            print "Insert ingredient name for a specific ingredient or don't for next option"
            Ingredient = raw_input("Ingredient> ")
            if Ingredient:
                return db.ingredients.get(name = Ingredient)
            else:
                print "insert restaurant_id for that restaurant's dishes' ingredients or don't for next option"
                RestaurantID = raw_input("RestaurantID> ")
                if RestaurantID:
                    restaurant = db.restaurants.get(restaurant_id = RestaurantID)
                    if restaurant:
                        print "insert dish name for that dish's ingredients or don't for all ingredients in all dishes of the restaurant"
                        DishName = raw_input("DishName> ")
                        if DishName:
                            return db.dishes.get(RestaurantID = RestaurantID, name = DishName)
                        else:
                            return db.dishes.get(RestaurantID = RestaurantID)
                    else:
                        print "Restaurant doesn't exit"
                else:
                    choice = raw_input("All Dishes? [Y/n]")
                    if choice in ["", "Y", "y"]:
                        print "PASCOA"
                        return db.ingredients.get()
                    else:
                        return []

    elif cmd == "I":
        try:
            if col == "U":
                username = ""
                password = ""
                fid = ""
                end = False
                while not username:
                    username = raw_input("Username> ")
                    if not username:
                        if end:
                            return False
                        else:
                            print "username necessessary, type <enter> again to leave"
                            end = True
                    elif end:
                        end = False
                while not password:
                    password = raw_input("Password> ")
                    if not password:
                        if end:
                            return False
                        else:
                            print "password necessessary, type <enter> again to leave"
                            end = True
                    elif end:
                        end = False
                while not fid:
                    fid = raw_input("FiscalID> ")
                    if not fid:
                        if end:
                            end = False
                            break
                        else:
                            print "are you sure? press <enter> to confirm"
                            end = True
                    elif end:
                        end = False
                user = {
                    "username": username,
                    "password": password,
                    "fid": fid
                }
                return db.users.insert(username=username, password=password, fid=fid)

            elif col == "R":
                while not name:
                    username = raw_input("Name> ")
                    if not name:
                        if end:
                            return False
                        else:
                            print "name necessessary, type <enter> again to leave"
                            end = True
                    elif end:
                        end = False
                while not address:
                    address = raw_input("Address> ")
                    if not address:
                        if end:
                            return False
                        else:
                            print "address necessessary, type <enter> again to leave"
                            end = True
                    elif end:
                        end = False
                id = uuid.uuid4()
                restaurant = {
                    "name": name,
                    "address": address,
                    "id": id
                }
                return db.restaurants.insert(id=id, name=name,address=address)

            elif col == "D":
                restaurant = {}
                name = ""
                cost = -1.0
                calorias = -1

                while not restaurant:
                    restaurant_id = raw_input("RestaurantID> ")
                    if not restaurant_id:
                        if end:
                            return False
                        else:
                            print "restaurant_id necessessary, type <enter> again to leave"
                            end = True
                    else:
                        restaurant = db.restaurants.get(RestaurantID = restaurant_id)
                        if not restaurant:
                            print "restaurant doesn't exist"
                        if end:
                            end = False

                while not name:
                    username = raw_input("Name> ")
                    if not name:
                        if end:
                            return False
                        else:
                            print "name necessessary, type <enter> again to leave"
                            end = True
                    elif end:
                        end = False

                while cost == -1.0:
                    try:
                        cost = float(raw_input("Cost> "))
                    except:
                        print "invalid value"
                    if not cost:
                        if end:
                            return False
                        else:
                            print "cost necessessary, type <enter> again to leave"
                            end = True
                    elif end:
                        end = False

                while calories == -1:
                    try:
                        calories = int(raw_input("Calories> "))
                    except:
                        print "invalid value"
                    if not cost:
                        if end:
                            return False
                        else:
                            print "calories necessessary, type <enter> again to leave"
                            end = True
                    elif end:
                        end = False

                dish = {
                    "restaurant": restaurant_id,
                    "name": name,
                    "cost": cost,
                    "calories": calories
                }
            elif col == "I":
                name = ""
                type = ""
                while not name:
                    name = raw_input("Ingredient> ")
                    if not name:
                        if end:
                            return False
                        else:
                            print "name necessessary, type <enter> again to leave"
                            end = True
                    elif end:
                        end = False
                while not type:
                    type = raw_input("Type> ")
                    if not type:
                        if end:
                            return False
                        else:
                            print "type necessessary, type <enter> again to leave"
                            end = True
                    else:
                        if type not in ["meat", "fish", "vegetarian"]:
                            print "invalid type"
                            print "types: meat/fish/vegetarian"
                        if end:
                            end = False
                alergens = []
                while True:
                    allergen = raw_input("Add Alergen> ")
                    if allergen:
                        allergens.append(allergen)
                        if end:
                            end = False
                    else:
                        if end:
                            end = False
                            break
                        else:
                            print "you sure? press <enter> to confirm"
                            end = True

                while not description:
                    description = raw_input("Description> ")
                    if not description:
                        if end:
                            end = False
                            break
                        else:
                            print "you sure? press <enter> to confirm"
                            end = True
                ingredient = {
                    "name": name,
                    "type": type,
                    "allergens": allergens,
                    "description": description
                }
                db.ingredients.insert(ingredient)

        except Exception as e:
            print "Command Insert"
            return False

    elif cmd == "U":
        if col == "U":
            pass

        elif col == "R":
            pass

        elif col == "D":
            pass

        elif col == "I":
            pass

    elif cmd == "D":
        try:
            if col == "U":
                print "insert username for a specific user or don't for all users"
                username = raw_input("Username> ")
                if username:
                    return db.users.remove(username)
                else:
                    return db.users.remove()
            elif col == "R":
                print "insert restaurant_id for a specific user or don't for all restaurants"
                restaurant_id = raw_input("RestaurantID> ")
                if restaurant_id:
                    return db.restaurants.remove(username)
                else:
                    return db.restaurants.remove()
            elif col == "D":
                print "insert restaurant for the dishes of a restaurant or don't for all the restaurants"
                restaurant_id = raw_input("RestaurantID> ")
                if restaurant_id:
                    return db.restaurants.remove(username)
                else:
                    return db.restaurants.remove()
            elif col == "I":
                print "insert ingredient or don't for all the ingredients"
                ingredient = raw_input("Ingredient> ")
                if ingredient:
                    return db.ingredients.remove(ingredients)
                else:
                    return db.ingredients.remove()
        except Exception as e:
            print "Command Delete"
            print e
            return False

def main():
    db = Database()
    end = False
    print_commands()
    while not end:
        cmd = raw_input("> ")
        if cmd:
            cmd = cmd.split()
            if cmd[0] in ["G","I","U","D"] and len(cmd) == 2:
                if cmd[1] in ["U", "R", "D", "I"]:
                    print command(db, cmd[0], cmd[1])
            elif cmd[0] == "M" and len(cmd) == 1:
                print_commands(True)
            elif cmd[0] == "L" and len(cmd) == 1:
                load(db)
            elif cmd[0] == "R" and len(cmd) == 1:
                db.users.remove()
                db.restaurants.remove()
                db.dishes.remove()
                db.ingredients.remove()
            elif cmd[0] == "E" and len(cmd) == 1:
                end = True
            else:
                print_commands()

if __name__ == "__main__":
    main()
