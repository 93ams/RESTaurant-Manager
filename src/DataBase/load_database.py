users = [{
            "username": "tilau",
            "password": "asd",
            "fid": "5235ujh3553"
        },{
            "username": "mimi",
            "password": "mimixu",
            "fid": "25vb5bi4ut4"
        },{
            "username": "pascoa",
            "password": "dsa",
            "fid": "dsad978a9dsds"
        }]

restaurants = [{
                "name": "casa bonita",
                "restaurant_id": "asd-dsa-asd-321ds-dsa",
                "address": "last of the mehicans St"
            },{
                "name": "tasca da mimi",
                "restaurant_id": "asdfs-2424-dsad-23asd",
                "address": "rua sexytime fofinha mimixuuu"
            }]

bife = {"name": "bife",
        "type": "meat"}

sardinha = {"name": "sardinha",
            "type": "fish"}

ovos = {"name": "ovos",
        "type": "meat"}

batata = {"name": "batata",
          "type": "vegetarian"}

alface = {"name": "alface",
          "type": "vegetarian" }

tomate = {"name": "tomate",
          "type": "vegetarian"}

arroz = {"name": "arroz",
         "type": "vegetarian"}

pao = {"name": "pao",
       "type": "vegetarian"}

ingredients = [bife, sardinha, ovos, batata, arroz, pao]

dishes = [{
            "name": "bitoque",
            "restaurant": "asd-dsa-asd-321ds-dsa",
            "cost": 3.99,
            "calories": 874,
            "ingredients": [pao, ovos, batata, bife, arroz]
        },{
            "name": "sardinha no pao",
            "restaurant": "asd-dsa-asd-321ds-dsa",
            "cost": 2.79,
            "calories": 537,
            "ingredients": [sardinha, pao, batata]
        },{
            "name": "salada de tomate com arroz",
            "restaurant": "asdfs-2424-dsad-23asd",
            "cost": 1.99,
            "calories": 2,
            "ingredients": [alface, tomate, arroz]
        }]


def load(db):
    for user in users:
        db.users.insert(user)
    for restaurant in restaurants:
        db.restaurants.insert(restaurant)
    for ingredient in ingredients:
        db.ingredients.insert(ingredient)
    for dish in dishes:
        db.dishes.insert(dish)
