from flask import Blueprint, request
from sqlmodel import Session, select

from db import engine
from models import CarModel, OwnerModel

owner_route = Blueprint('owner', __name__)


@owner_route.route('/')
def owner():
    session = Session(engine)
    query = select(OwnerModel)
    owners = session.exec(query).all()

    owners_list = []

    for owner in owners:
        owner_data = owner.model_dump()

        cars = session.exec(
            select(CarModel).where(CarModel.owner_id == owner.id)
        ).all()

        if len(cars) == 1:
            owner_data['status'] = f'The owner has {len(cars)} car'
        elif len(cars) > 1:
            owner_data['status'] = f'The owner has {len(cars)} cars'
        else:
            owner_data['status'] = 'Sale opportunity'

        owners_list.append(owner_data)

    session.close()
    return owners_list


@owner_route.route('/', methods=['POST'])
def add_owner():
    session = Session(engine)
    data = request.get_json()
    name = data.get('name')
    if not name:
        return {'message': 'Name is required'}, 400
    owner = OwnerModel(name=name)

    session.add(owner)
    session.commit()

    session.refresh(owner)
    session.close()
    return owner.model_dump(), 201


@owner_route.route('/<int:owner_id>')
def view_owner(owner_id: int):
    session = Session(engine)

    query = select(OwnerModel).where(OwnerModel.id == owner_id)
    owner = session.exec(query).first()

    session.close()
    if not owner:
        return {'message': 'Owner not found'}, 404

    cars = session.exec(
        select(CarModel).where(CarModel.owner_id == owner_id)
    ).all()
    cars_list = []
    for car in cars:
        cars_list.append(car.model_dump())

    owner_data = owner.model_dump()
    owner_data['cars'] = cars_list

    if len(cars) == 1:
        owner_data['status'] = f'The owner has {len(cars)} car'
    elif len(cars) > 1:
        owner_data['status'] = f'The owner has {len(cars)} cars'
    else:
        owner_data['status'] = 'Sale opportunity'

    return owner_data


@owner_route.route('/<int:owner_id>', methods=['PATCH'])
def update_owner(owner_id: int):
    session = Session(engine)

    query = select(OwnerModel).where(OwnerModel.id == owner_id)
    owner = session.exec(query).first()

    if not owner:
        return {'message': 'Owner not found'}, 404

    data = request.get_json()
    name = data.get('name')
    if not name:
        return {'message': 'Name is required'}, 400
    owner.name = name
    session.add(owner)
    session.commit()
    session.refresh(owner)
    session.close()

    return owner.model_dump(), 201


@owner_route.route('/<int:owner_id>', methods=['DELETE'])
def delete_owner(owner_id: int):
    session = Session(engine)

    query = select(OwnerModel).where(OwnerModel.id == owner_id)
    owner = session.exec(query).first()
    if not owner:
        return {'message': 'Owner not found'}, 404

    cars = session.exec(
        select(CarModel).where(CarModel.owner_id == owner_id)
    ).all()
    for car in cars:
        session.delete(car)

    session.delete(owner)
    session.commit()

    session.close()

    return owner.model_dump(), 204
