import datetime
import os

import bcrypt
import jwt
from dotenv import load_dotenv
from flask import Blueprint, request
from sqlmodel import Session, select

from db import engine
from models import UserModel

user_route = Blueprint('user', __name__)
load_dotenv()


@user_route.route('/', methods=['POST'])
def login():
    session = Session(engine)
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {'message': 'Username and password is required'}, 400

    user = session.exec(
        select(UserModel).where(UserModel.username == username)
    ).first()
    if not user:
        return {'message': 'User not found'}, 404
    if not bcrypt.checkpw(password.encode(), bytes(user.password)):
        return {'message': 'Incorrect password'}, 401

    expiration = datetime.datetime.now(
        tz=datetime.timezone.utc
    ) + datetime.timedelta(minutes=int(os.getenv('JWT_EXPIRATION', 15)))
    user_data = {'username': user.username, 'id': user.id, 'exp': expiration}

    encoded = jwt.encode(
        user_data, os.getenv('JWT_SECRET_KEY', 'key'), algorithm='HS256'
    )

    session.close()

    return {'access_token': encoded}
