#!/usr/bin/env python
from ming import create_datastore
from ming.odm import ThreadLocalODMSession

session = ThreadLocalODMSession(
    bind = create_datastore('mongodb://localhost:27017/RESTaurant_Manager')
)

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty,  RelationProperty

class User(MappedClass):
    class __mongometa__:
        session = session
        name = 'user'

    _id = FieldProperty(schema.ObjectId)

    username = FieldProperty(schema.String(required=True))
    password = FieldProperty(schema.String(required=True))
    fid = FieldProperty(schema.String(required=True))
    manager = FieldProperty(schema.Bool(required=True))

    restaurant_id = ForeignIdProperty('Restaurant')
    restaurant = RelationProperty('Restaurant')

class Restaurant(MappedClass):
    class __mongometa__:
        session = session
        name = 'restaurant'

    _id = FieldProperty(schema.ObjectId)

    restaurant_id = FieldProperty(schema.String(required=True))
    name = FieldProperty(schema.String(required=True))
    address = FieldProperty(schema.String(required=True))

    manager_ids = ForeignIdProperty('User', uselist=True)
    managers = RelationProperty('User')

    dishes = RelationProperty('Dish')

class Dish(MappedClass):
    class __mongometa__:
        session = session
        name = 'dish'

    _id = FieldProperty(schema.ObjectId)

    name = FieldProperty(schema.String(required=True))
    rate = FieldProperty(schema.Float())
    cost = FieldProperty(schema.Float())
    calories = FieldProperty(schema.Int())

    restaurant_id = ForeignIdProperty('Restaurant')
    restaurant = RelationProperty('Restaurant')

    ingredient_ids = ForeignIdProperty('Ingredient', uselist=True)
    ingredients = RelationProperty('Ingredient')

class Ingredient(MappedClass):
    class __mongometa__:
        session = session
        name = 'ingredient'

    _id = FieldProperty(schema.ObjectId)

    name = FieldProperty(schema.String(required=True))
    type = FieldProperty(schema.OneOf("vegetarian", "fish", "meat"))
    allergens = FieldProperty(schema.Array(schema.String(if_missing='')))
    description = FieldProperty(schema.String(if_missing=''))
