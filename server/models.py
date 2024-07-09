from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')
    pizzas = db.relationship('Pizza', secondary='restaurant_pizza', back_populates='restaurants')

    serialize_rules = ('-restaurant_pizzas.restaurant', '-restaurant_pizzas.pizza')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location
        }

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza', cascade='all, delete-orphan')
    restaurants = db.relationship('Restaurant', secondary='restaurant_pizza', back_populates='pizzas')

    serialize_rules = ('-restaurant_pizzas.restaurant', '-restaurant_pizzas.pizza')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizza'
    
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id', ondelete='CASCADE'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas')

    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")
        return price

    def to_dict(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'pizza_id': self.pizza_id,
            'price': self.price
        }
    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
