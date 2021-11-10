from flask import Blueprint, request, jsonify
from car_inventory.helpers import token_required
from car_inventory.models import db, User, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata():
    return {'some':"value"}

# CREATE CAR ROUTE
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_production = request.json['cost_of_production']
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    user_token = current_user_token.token

    car = Car(name, description, price, max_speed, dimensions, weight, cost_of_production, make, model, year, user_token)
    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)
    
# Retrieve all car endpoint
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    car = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(car)
    return jsonify(response)

# Retrieve single car endpoint
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid token required'}), 401


# Update car endpoint
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id) #Get the drone instance

    car.name = request.json['name']
    car.description = request.json['description']
    car.price = request.json['price']
    car.max_speed = request.json['max_speed']
    car.dimensions = request.json['dimensions']
    car.weight = request.json['weight']
    car.cost_of_production = request.json['cost_of_production']
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete car endpoint
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)