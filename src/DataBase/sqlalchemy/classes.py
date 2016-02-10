from sqlalchemy import create_engine
from sqlalchemy import Table, Column, and_
from sqlalchemy import Integer, String, Float
from sqlalchemy import ForeignKey, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    username = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship('Restaurant')
    def json(self):
        doc = {
            "username": self.username,
            "name": self.name,
            "password": self.password
        }
        if self.restaurant:
            doc["restaurant"] = self.restaurant.name
        return doc

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique = True)
    address = Column(String, nullable=False)

    managers = relationship("User")
    dishes = relationship("Dish")

    def json(self):
        doc = {
            "name": self.name,
            "address": self.address,
            "managers": [manager.username for manager in self.managers],
            "dishes": [dish.name for dish in self.dishes]
        }
        return doc

dish2ingredient = Table('dish_ingredient_link', Base.metadata,
      Column('restaurant_id', Integer, primary_key=True),
      Column('dish_name', String, primary_key=True),
      ForeignKeyConstraint(('restaurant_id', 'dish_name'),
                           ('dish.restaurant_id', 'dish.name')),
      Column('ingredient_name', String, ForeignKey('ingredient.id'), primary_key=True),
)

class Dish(Base):
    __tablename__ = 'dish'

    name = Column(String, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'), primary_key=True)
    restaurant = relationship("Restaurant")

    cost = Column(Float, nullable=False)
    calories = Column(Integer, nullable=False)

    ingredients = relationship('Ingredient',
                                secondary = dish2ingredient,
                                backref="dishes")
    def json(self):
        doc = {
            "name": self.name,
            "cost": self.cost,
            "calories": self.calories,
            "ingredients": [ingredient.name for ingredient in self.ingredients]
        }
        return doc

class Ingredient(Base):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    type = Column(String, nullable=False)

    def json(self):
        doc = {
            "name": self.name,
            "type": self.type
        }
        return doc


engine = create_engine('sqlite:///../sqlite/sqlite.db', echo = False)
Base.metadata.create_all(engine)
