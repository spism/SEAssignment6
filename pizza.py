import flask


class Pizza:

    def _init_(self, pizza_id, name, vegetarian, price,toppings):
        self.pizza_id = pizza_id
        self.name = name
        self.vegetarian = vegetarian
        self.price = price
        self.toppings = toppings

    def to_json(self):
        d = {
            "pizza_id": self.pizza_id,
            "name": self.name,
            "vegetarian": self.vegetarian,
            "price": self.price,
            "toppings": "none"
        }
        js = flask.jsonify(d)
        js.status_code = 200
        return js

    def get_id(self):
        return self.pizza_id
