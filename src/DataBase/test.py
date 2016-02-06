from database import Database
import uuid

def print_commands():
    print "Commands: "
    print "G: Get"
    print "I: Insert"
    print "U: Update"
    print "D: Delete"
    print "L: Load"
    print "R: Reset"
    print "E: Exit"
    print " ----------------------------------------------------------------------------------------------------- "
    print " | [cmd] | [collection] |              [input(s)]                         ||       Description       | "
    print " |-------|--------------|-------------------------------------------------||-------------------------| "
    print " |   G   |      U       | [-u] [Username]                                 || Gets user(s)            | "
    print " |   G   |      R       | [-i] [RestaurantID] [-n] [Name]                 || Gets restaurant(s)      | "
    print " |   I   |      U       | [-u] Username [-p] Password                     || Insert a new user       | "
    print " |   I   |      R       | [-i] RestaurantID [-n] Name [-a] Address        || Insert a new restaurant | "
    print " |   U   |      U       | [-u] Username [-p] [Password]                   || Updates user            | "
    print " |   U   |      R       | [-i] RestaurantID [-n] [Name] [-a] [Address]    || Updates restaurant      | "
    print " |   D   |      U       | [-u] [Username]                                 || Deletes user(s)         | "
    print " |   D   |      R       | [-i] [RestaurantID]                             || Deletes restaurant(s)   | "
    print " |   L   |      -       | [-f] Filepath                                   || Loads content from file | "
    print " |   R   |      -       |                                                 || Resets the database     | "
    print " |   E   |      -       |                                                 || Exit the program        | "
    print " ----------------------------------------------------------------------------------------------------- "

def main():
    db = Database()
    end = False
    print_commands()
    while not end:
        cmd = raw_input("> ")
        if cmd:
            cmd = cmd.split()
            if cmd[0] == "G" and len(cmd) > 1 and len(cmd) < 9:
                if cmd[1] == "U":
                    try:
                        index = cmd.index("-u")
                        username = cmd[index + 1]
                    except:
                        username = ""

                    if username:
                        print db.users.get(username = username)
                    else:
                        print db.users.get()

                elif cmd[1] == "R":
                    try:
                        index = cmd.index("-i")
                        RestaurantID = cmd[index + 1]
                    except:
                        RestaurantID = ""

                    try:
                        index = cmd.index("-n")
                        Name = cmd[index + 1]
                    except:
                        Name = ""

                    if RestaurantID:
                        print db.restaurants.get(RestaurantID = RestaurantID)
                    elif Name:
                        print db.restaurants.get(RestaurantName = Name)
                    else:
                        print db.restaurants.get()
                else:
                    print_commands()

            elif cmd[0] == "I" and len(cmd) > 1 and len(cmd) < 9:
                if cmd[1] == "U":
                    try:
                        index = cmd.index("-u")
                        username = cmd[index + 1]
                    except:
                        username = ""
                    try:
                        index = cmd.index("-p")
                        password = cmd[index + 1]
                    except:
                        password = ""

                    if username and password:
                        try:
                            print db.users.insert(username, password)
                        except Exception as e:
                            print e
                    else:
                        pass

                elif cmd[1] == "R":
                    try:
                        index = cmd.index("-i")
                        RestaurantID = cmd[index + 1]
                    except:
                        RestaurantID = ""

                    try:
                        index = cmd.index("-n")
                        Name = cmd[index + 1]
                    except:
                        Name = ""

                    try:
                        index = cmd.index("-a")
                        Address = cmd[index + 1]
                    except:
                        Address = ""

                    if RestaurantID and Name and Address:
                        try:
                            id = str(uuid.uuid4())
                            db.restaurants.insert(id, Name, Address)
                        except Exception as e:
                            print e
                else:
                    print_commands()

            elif cmd[0] == "U" and len(cmd) > 1 and len(cmd) < 9:
                if cmd[1] == "U":
                    try:
                        index = cmd.index("-u")
                        username = cmd[index + 1]
                    except:
                        username = ""
                    try:
                        index = cmd.index("-u")
                        username = cmd[index + 1]
                    except:
                        username = ""

                    if username:
                        pass
                    else:
                        pass

                elif cmd[1] == "R":
                    try:
                        index = cmd.index("-i")
                        RestaurantID = cmd[index + 1]
                    except:
                        RestaurantID = ""

                    try:
                        index = cmd.index("-n")
                        Name = cmd[index + 1]
                    except:
                        Name = ""

                    try:
                        index = cmd.index("-a")
                        Address = cmd[index + 1]
                    except:
                        Address = ""
                else:
                    print_commands()

            elif cmd[0] == "D" and len(cmd) > 1 and len(cmd) < 5:
                if cmd[1] == "U":
                    try:
                        index = cmd.index("-u")
                        username = cmd[index + 1]
                    except:
                        username = ""
                    if username:
                        db.users.remove(username = username)
                    else:
                        db.users.remove()

                elif cmd[1] == "R":
                    try:
                        index = cmd.index("-i")
                        RestaurantID = cmd[index + 1]
                    except:
                        RestaurantID = ""

                    if RestaurantID:
                        db.restaurants.remove(RestaurantID)
                    else:
                        db.restaurants.remove()
                else:
                    print_commands()

            elif cmd[0] == "R" and len(cmd) == 1:
                db.users.remove()
                db.restaurants.remove()
            elif cmd[0] == "E" and len(cmd) == 1:
                end = True
            else:
                print_commands()

if __name__ == "__main__":
    main()
