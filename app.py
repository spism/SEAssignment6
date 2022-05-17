from flask import Flask, request, jsonify, make_response, render_template
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

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/pizza')
def get_pizzas():  # put application's code here
    return make_response({"list of pizzas": [pizza.to_dict() for pizza in pizzas.get_objects()]},200)


@app.route('/pizza/<pizza_id>', methods = ["GET"])
def get_pizza(pizza_id: int):

    pizza = pizzas.get_object(int(pizza_id))
    if pizza is None:
        return make_response({"message": "pizza not found"},404)
    else:
        return make_response(pizza.to_dict(),200)


@app.route('/order/<order_id>', methods = ["GET"])
def get_order(order_id: int):

    try:
        order = orders.get_object(int(order_id))

        if order is None:
            return make_response(json.dumps({"message": "Order_ID not found"}),404)
        else:
            return make_response(order.to_dict(),200)

    except:
        return make_response(json.dumps({"message": "Invalid ID supplied"}), 400)


@app.route('/order', methods=["POST"])
def new_order():
    global order_id

    try:
        data = request.get_json()

        pizza_list = [pizzas.get_object(pizza_id)  for pizza_id in data["pizzas"]]
        takeaway = data["takeaway"]
        payment_type = data["payment_type"]
        customer_id = data["customer_id"]
        note = data["note"]
        delivery_address = data["delivery_address"]

        # check the format of delivery address
        if "street" not in delivery_address or "city" not in delivery_address or "country" not in delivery_address or "zipcode" not in delivery_address:
            raise

        o = Order(order_id, customer_id, "In Progress", datetime.now(), note, takeaway, payment_type, delivery_address, pizza_list)
        order_id += 1
        orders.add_object(o)

        d = {
            "order": o.to_dict(),
            "ordered_at": o.ordered_at,
            "delivery_time": o.ordered_at.replace(hour = o.ordered_at.hour + 1)
        }
        return make_response(d,200)
    except:
        return make_response({"message": "The format of the object is not valid"},400)


@app.route('/order/cancel/<order_id>', methods = ["PUT"])
def cancel_order(order_id: int):
    order = orders.get_object(int(order_id))
    if order is None:
        return make_response({"message": "Order not found"},404)
    if order.status == "cancelled" or order.status == "delivered":
        return make_response({"message": "Unable to cancel an already canceled or delivered order"},422)

    diff = (datetime.now() - order.ordered_at).total_seconds()
    if diff > 300:
        return make_response({"message": "Unable to cancel your order after 5 minutes have elapsed."},412)
    else:
        order.status = "cancelled"
        orders.update_object(int(order_id),order)
        return make_response({"order_id": order.get_id(), "status": "cancelled" },200)


@app.route('/order/deliverytime/<order_id>', methods = ["GET"])
def get_delivery_time(order_id : int):
    order = orders.get_object(int(order_id))
    if order is None:
        return make_response({"message": "Order not found"},404)
    else:
        estimated_delivery_time = datetime.now()
        estimated_delivery_time = estimated_delivery_time.replace(hour=estimated_delivery_time.hour+ 1)
        d = {
            "order": order.to_dict(),
            "delivery_time": estimated_delivery_time
        }
        return make_response(d,200)

@app.route('/order/delivered/<order_id>', methods = ["PUT"])
def deliver_order(order_id: int):
    order = orders.get_object(int(order_id))
    if order is None:
        return make_response({"message": "Order not found"},404)
    if order.status == "cancelled" or order.status == "delivered":
        return make_response({"message": "Unable to deliver an already canceled or delivered order"},422)

    order.status = "delivered"
    orders.update_object(int(order_id),order)
    return make_response({"order_id": order.get_id(), "status": "delivered" },200)



if __name__ == '__main__':
    app.run()

