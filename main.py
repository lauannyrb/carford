import os

from dotenv import load_dotenv
from flask import Flask

from middlewares import authorization_middleware
from routes.car import car_route
from routes.owner import owner_route
from routes.user import user_route

app = Flask(__name__)
app.before_request(authorization_middleware)

app.register_blueprint(owner_route, url_prefix='/owner')
app.register_blueprint(car_route, url_prefix='/car')
app.register_blueprint(user_route, url_prefix='/')

load_dotenv()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('API_PORT', 5000), host='0.0.0.0')
