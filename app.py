from flask import Flask, request
from order import Order
from database import Database
from datetime import datetime
import json

app = Flask(__name__)

orders = Database("Orders")
pizzas = Database("Pizzas")
order_id = 0


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
    global order_id

    pizzas = request.form["pizzas"]
    takeaway = request.form["takeaway"]
    payment_type = request.form["payment_type"]
    customer_id = request.form["customer_id"]
    note = request.form["note"]
    delivery_address = request.form["delivery_address"]
    o = Order(order_id, customer_id, "ordered", datetime.now(), note, takeaway, payment_type, delivery_address, pizzas)
    order_id += 1
    orders.add_object(o)


@app.route('/order/cancel/{order_id}', methods = ["PUT"])
def cancel_order(order_id: int):
    pass


@app.route('/order/deliverytime/{order_id}', methods = ["GET"])
def get_delivery_time(order_id : int):
    pass




if __name__ == '__main__':
    app.run()

