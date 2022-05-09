from flask import *
import json

class Pizza:

    def __init__(self, pizza_id, name, vegetarian, price,toppings):
        self.pizza_id = pizza_id
        self.name = name
        self.vegetarian = vegetarian
        self.price = price
        self.toppings = toppings

    def get_id(self):
        return self.pizza_id

    def to_json(self):
        d = {
            "pizza_id": self.pizza_id,
            "name": self.name,
            "vegetarian": self.vegetarian,
            "price": self.price,
            "toppings": self.toppings
        }
        js = json.dumps(self.__dict__)
        return js
