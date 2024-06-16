import os

import jwt
from dotenv import load_dotenv
from flask import request

from utils import abort_request

load_dotenv()

def authorization_middleware():
    if not request.path == '/':
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            abort_request('No header authorization', 400)
        try:
            jwt.decode(authorization_header, os.getenv('JWT_SECRET_KEY', 'key'), algorithms=["HS256"])   
        except jwt.exceptions.InvalidSignatureError:
            abort_request('Invalid jwt token', 400)
        except jwt.exceptions.ExpiredSignatureError:
            abort_request('Signature has expired', 400)
