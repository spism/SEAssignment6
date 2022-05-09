from flask import Flask, request
from pizza import Pizza
from database import Database
import json

app = Flask(__name__)

orders = Database("Orders")
pizzas = Database("Pizzas")


@app.route('/pizza')
def get_pizzas(pizza_id, name, vegetarian, price, toppings):  # put application's code here
    return json.dumps([pizza.__dict__ for pizza in pizzas.get_objects()])

@app.route('/pizza/{pizza_id}', methods = ["GET"])
def get_pizza(pizza_id: int):
    return pizzas.get_object(pizza_id).to_json()


@app.route('/order/{order_id}', methods = ["GET"])
def get_order(order_id: int):
    return orders.get_object(order_id)


@app.route('/order', methods=["POST"])
def new_order():
    pizzas = request.form["pizzas"]
    orders.add_object()


@app.route('/order/cancel/{order_id}', methods = ["PUT"])
def cancel_order(order_id: int):
    pass


@app.route('/order/deliverytime/{order_id}', methods = ["GET"])
def get_delivery_time(order_id : int):
    pass




if __name__ == '__main__':
    app.run()

