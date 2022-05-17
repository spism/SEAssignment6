import json

import flask
import pizza


class Order:

    def __init__(self,order_id, customer_id,status,ordered_at,note,takeaway,payment_type,delivery_address, pizzas):
        self.order_id = order_id
        self.customer_id = customer_id
        self.status = status
        self.ordered_at = ordered_at
        self.note = note
        self.takeaway = takeaway
        self.payment_type = payment_type
        self.delivery_address = delivery_address
        self.pizzas = pizzas


    def get_id(self):
        return self.order_id

    def to_dict(self):
        pizza_json = [pizza.to_dict() for pizza in self.pizzas]
        d = {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "status": self.status,
            "ordered_at": self.ordered_at,
            "note": self.note,
            "takeaway": self.takeaway,
            "payment_type": self.payment_type,
            "delivery_address": self.delivery_address,
            "pizzas": pizza_json
        }
        return d
