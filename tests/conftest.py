import os

import pytest
from flask import Flask


@pytest.fixture(scope='session')
def app():
    with open('testing', 'w') as file:
        file.write('')
    from main import app as flask_app

    yield flask_app
    os.remove('testing')
    if os.path.isfile('data/database_test.sqlite'):
        os.remove('data/database_test.sqlite')


@pytest.fixture(scope='session')
def client(app: Flask):
    test_client = app.test_client()
    return test_client


@pytest.fixture(scope='session')
def access_token(client):
    response = client.post(
        '/', json={'username': 'admin', 'password': 'admin'}
    )
    access_token = response.get_json()
    return access_token['access_token']
