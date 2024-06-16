from flask import Blueprint, request
from sqlmodel import Session, select

from db import engine
from models import CarModel, OwnerModel

car_route = Blueprint('car', __name__)

@car_route.route('/')
def car():
   session = Session(engine)
   query = select(CarModel)
   cars = session.exec(query).all()
   
   cars_list = []
   for car in cars:
       cars_list.append(car.model_dump())

   session.close()
   return cars_list

@car_route.route('/', methods=['POST'])
def add_car():
    session = Session(engine)
    data = request.get_json()

    color = data.get('color')
    available_colors = ["yellow", "blue", "gray"]
    if color not in available_colors:
        return {"message": f"Invalid or missing color. Available colors: {', '.join(available_colors)}"}, 400

    model = data.get('model')
    available_models = ["hatch", "sedan", "convertible"]
    if model not in available_models:
        return {"message": f"Invalid or missing model. Available models: {', '.join(available_models)}"}, 400

    owner_id = data.get('owner_id')
    owner = session.exec(select(OwnerModel).where(OwnerModel.id == owner_id)).first()
    if not owner:
        return {"message": "Owner not found"}, 404
    
    owner_cars = session.exec(select(CarModel).where(CarModel.owner_id == owner_id)).all()
    if len(owner_cars) == 3:
        return {"message": "Owner has the maximum number of cars (3)"}, 409
    
    car = CarModel(color=color, model=model, owner_id=owner_id)
    session.add(car)
    session.commit()

    session.refresh(car)
    session.close()

    return car.model_dump(), 201

@car_route.route('/<int:car_id>')
def view_car(car_id:int):

    session = Session(engine)
    car = session.exec(select(CarModel).where(CarModel.id == car_id)).first()

    session.close()

    if not car:
        return {"message": "Car not found"}, 404
    return car.model_dump()

@car_route.route('/<int:car_id>', methods=['PATCH'])
def update_car(car_id:int):
    session = Session(engine)
    data = request.get_json()
    
    car = session.exec(select(CarModel).where(CarModel.id == car_id)).first()
    if not car:
        return {'messagem': 'Car not found'}, 404
    
    color = data.get('color')
    available_colors = ["yellow", "blue", "gray"]
    if color not in available_colors:
        return {"message": f"Invalid or missing color. Available colors: {', '.join(available_colors)}"}, 400

    model = data.get('model')
    available_models = ["hatch", "sedan", "convertible"]
    if model not in available_models:
        return {"message": f"Invalid or missing model. Available models: {', '.join(available_models)}"}, 400

    owner_id = data.get('owner_id')
    owner = session.exec(select(OwnerModel).where(OwnerModel.id == owner_id)).first()    
    if not owner:
        return {"message": "Owner not found"}, 404
    
    owner_cars = session.exec(select(CarModel).where(CarModel.owner_id == owner_id)).all()
    if len(owner_cars) == 3:
        return {"message": "Owner has the maximum number of cars (3)"}, 409
    
    car.color = color
    car.model = model
    car.owner_id = owner_id
    
    session.add(car) 
    session.commit()

    session.refresh(car)
    session.close()

    return car.model_dump()

@car_route.route('/<int:car_id>', methods=['DELETE'])
def delete_car(car_id:int):
    session = Session(engine)
    
    car = session.exec(select(CarModel).where(CarModel.id == car_id)).first()
    if not car:
        return {'message': 'Car not found'}, 404
    
    session.delete(car)
    session.commit()
    session.close()
    
    return car.model_dump(), 204