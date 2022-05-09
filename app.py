from flask import Flask, request
from pizza import Pizza
from database import Database

app = Flask(__name__)

orders = Database("Orders")
pizzas = Database("Pizzas")


@app.route('/pizza')
def get_pizzas(pizza_id, name, vegetarian, price, toppings):  # put application's code here
    return orders


@app.route('/pizza/{pizza_id}')
def get_pizza(pizza_id: int):
    return pizzas.get_object(pizza_id)


@app.route('/order/{order_id}')
def get_order(order_id: int):
    return orders.get_object(order_id)


@app.route('/order', methods=["POST"])
def new_order():
    pizzas = request.form["pizzas"]
    
    orders.add_object()


if __name__ == '__main__':
    app.run()

