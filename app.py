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

@app.route("/order/create")
def create_order():
    return render_template("create_order.html")

@app.route("/order/display", methods = ['POST'])
def display_order():
    return make_response(request.form, 200)

@app.route('/pizza')
def get_pizzas():  # put application's code here
    return make_response({"list of pizzas": [pizza.to_dict() for pizza in pizzas.get_objects()]},200)


@app.route('/pizza/<pizza_id>', methods = ["GET"])
def get_pizza(pizza_id: int):

    pizza = pizzas.get_object(int(pizza_id))
    if pizza is None:
        return make_response({"message": "pizza not found"},404)
    else:
        return make_response(pizza.__dict__,200)


@app.route('/order/<order_id>', methods = ["GET"])
def get_order(order_id: int):
    order = orders.get_object(int(order_id))

    if order is None:
        return make_response(json.dumps({"message": "order not found"}),404)
    else:
        return make_response(order.to_dict(),200)


@app.route('/order', methods=["POST"])
def new_order():
    global order_id

    try:
        data = request.get_json()

        pizza_list = [pizzas.get_object(pizza_id) for pizza_id in data["pizzas"]]
        takeaway = data["takeaway"]
        payment_type = data["payment_type"]
        customer_id = data["customer_id"]
        note = data["note"]
        delivery_address = data["delivery_address"]

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
        return json.dumps({"message": "Order not found"})
    if order.status == "cancelled" or order.status == "delivered":
        return json.dumps({"message": "Unable to cancel an already canceled or delivered order"})

    diff = (datetime.now() - order.ordered_at).total_seconds()
    if diff > 300:
        return json.dumps({"message": "Unable to cancel your order after 5 minutes have elapsed."})
    else:
        order.status = "cancelled"
        orders.update_object(int(order_id),order)
        return json.dumps({"order_id": order.get_id(), "status": "cancelled" })


@app.route('/order/deliverytime/<order_id>', methods = ["GET"])
def get_delivery_time(order_id : int):
    order = orders.get_object(int(order_id))
    if order is None:
        return json.dumps({"message": "Order not found"})
    else:
        estimated_delivery_time = datetime.now()
        estimated_delivery_time = estimated_delivery_time.replace(hour=estimated_delivery_time.hour+ 1)
        d = {
            "order": order.to_dict(),
            "delivery_time": estimated_delivery_time
        }
        return json.dumps(d)




if __name__ == '__main__':
    app.run()

