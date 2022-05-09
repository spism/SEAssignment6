from flask import Flask, request, jsonify
from order import Order
from pizza import Pizza
from database import Database
from datetime import datetime
import json

app = Flask(__name__)

orders = Database("Orders")
pizzas = Database("Pizzas")
order_id = 0

p1 = Pizza(1,"marga",True, 12.99, ["cheese","tomato sauce"])
p2 = Pizza(2,"hawaii",False,15.99,["cheese","pineapple","ham"])
pizzas.add_object(p1)
pizzas.add_object(p2)

@app.route('/pizza')
def get_pizzas():  # put application's code here
    return json.dumps([pizza.__dict__ for pizza in pizzas.get_objects()])


@app.route('/pizza/{pizza_id}', methods = ["GET"])
def get_pizza(pizza_id: int):
    return pizzas.get_object(pizza_id).to_json()


@app.route('/order/{order_id}', methods = ["GET"])
def get_order(order_id: int):
    return json.dumps(orders.get_object(order_id).__dict__)


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
    order = orders.get_object(order_id)
    if order is None:
        return json.dumps({"message": "Order not found"})
    if order.status == "cancelled" or order.status == "delivered":
        return json.dumps({"message": "Unable to cancel an already canceled or delivered order"})

    diff = (datetime.now() - order.ordered_at).total_seconds()
    if diff > 300:
        return json.dumps({"message": "Unable to cancel your order after 5 minutes have elapsed."})
    else:
        order.status = "cancelled"
        orders.update_object(order_id,object)
        return json.dumps({"order_id": order.get_id(), "status": "cancelled" })


@app.route('/order/deliverytime/{order_id}', methods = ["GET"])
def get_delivery_time(order_id : int):
    order = orders.get_object(order_id)
    if order is None:
        return json.dumps({"message": "Order not found"})
    else:
        estimated_delivery_time = datetime.now()
        estimated_delivery_time = estimated_delivery_time.replace(hour=estimated_delivery_time.hour+ 1)
        d = {
            "order": order.__dict__,
            "delivery_time": estimated_delivery_time
        }
        return json.dumps(d)




if __name__ == '__main__':
    app.run()

