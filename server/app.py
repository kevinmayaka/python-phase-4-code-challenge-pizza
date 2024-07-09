from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants])

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    return jsonify(restaurant.to_dict())

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({'message': 'Restaurant deleted successfully'}), 200

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    restaurant_id = data.get('restaurant_id')
    pizza_id = data.get('pizza_id')
    price = data.get('price')
    
    if not (1 <= price <= 30):
        return jsonify({'error': 'Price must be between 1 and 30'}), 400
    
    restaurant_pizza = RestaurantPizza(
        restaurant_id=restaurant_id,
        pizza_id=pizza_id,
        price=price
    )
    db.session.add(restaurant_pizza)
    db.session.commit()
    return jsonify(restaurant_pizza.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)
