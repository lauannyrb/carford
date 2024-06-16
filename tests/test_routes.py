from flask.testing import FlaskClient


def test_login_with_wrong_user(client: FlaskClient):
    response = client.post(
        '/', json={'username': 'admin_wrong', 'password': 'admin'}
    )
    assert response.status_code == 404


def test_login_with_wrong_password(client: FlaskClient):
    response = client.post(
        '/', json={'username': 'admin', 'password': 'admin_wrong'}
    )
    assert response.status_code == 401


def test_login_with_correct_user(client: FlaskClient):
    response = client.post(
        '/', json={'username': 'admin', 'password': 'admin'}
    )
    assert response.status_code == 200


def test_get_all_owners_without_login(client: FlaskClient):
    response = client.get('/owner')
    assert response.status_code == 400


def test_get_all_owners_with_access_token(
    client: FlaskClient, access_token: str
):
    response = client.get(
        '/owner',
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_create_owner_without_authentication(client: FlaskClient):
    response = client.post(
        '/owner', json={'name': 'Owner test'}, follow_redirects=True
    )
    assert response.status_code == 400


def test_create_owner_with_authentication(
    client: FlaskClient, access_token: str
):
    response = client.post(
        '/owner',
        json={'name': 'Owner test'},
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 201


def test_create_car_with_authentication(
    client: FlaskClient, access_token: str
):
    response = client.post(
        '/car',
        json={'color': 'blue', 'model': 'sedan', 'owner_id': 1},
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 201


def test_update_car_with_valid_color(client: FlaskClient, access_token: str):
    response = client.patch(
        '/car/1',
        json={'color': 'yellow', 'model': 'sedan', 'owner_id': 1},
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 201


def test_update_car_with_empty_body(client: FlaskClient, access_token: str):
    response = client.patch(
        '/car/1', json={}, headers={'Authorization': access_token}
    )
    assert response.status_code == 400


def test_update_car_with_invalid_color(client: FlaskClient, access_token: str):
    response = client.patch(
        '/car/1',
        json={'color': 'brown', 'model': 'sedan', 'owner_id': 1},
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 400


def test_update_car_with_valid_model(client: FlaskClient, access_token: str):
    response = client.patch(
        '/car/1',
        json={'color': 'yellow', 'model': 'hatch', 'owner_id': 1},
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 201


def test_update_car_with_invalid_model(client: FlaskClient, access_token: str):
    response = client.patch(
        '/car/1',
        json={'color': 'yellow', 'model': 'ferrari', 'owner_id': 1},
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 400


def test_creating_a_car_with_the_owner_having_3_cars(
    client: FlaskClient, access_token: str
):
    for _ in range(2):
        test_create_car_with_authentication(client, access_token)
    response = client.post(
        '/car',
        json={'color': 'blue', 'model': 'sedan', 'owner_id': 1},
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 409


def test_get_all_cars_before_delete_one_car(
    client: FlaskClient, access_token: str
):
    response = client.get(
        '/car', headers={'Authorization': access_token}, follow_redirects=True
    )
    assert len(response.get_json()) == 3


def test_delete_one_car(client: FlaskClient, access_token: str):
    response = client.delete(
        '/car/1',
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 204


def test_get_all_cars_after_delete_one_car(
    client: FlaskClient, access_token: str
):
    response = client.get(
        '/car', headers={'Authorization': access_token}, follow_redirects=True
    )
    assert len(response.get_json()) == 2


def test_delete_owner(client: FlaskClient, access_token: str):
    response = client.delete(
        '/owner/1',
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 204


def test_get_all_cars_after_delete_owner(
    client: FlaskClient, access_token: str
):
    response = client.get(
        '/car', headers={'Authorization': access_token}, follow_redirects=True
    )
    assert len(response.get_json()) == 0


# --


def test_create_car_without_authentication(client: FlaskClient):
    response = client.post(
        '/car', json={'color': 'blue', 'model': 'sedan', 'owner_id': 1}
    )
    assert response.status_code == 400


def test_create_car_with_invalid_color(client: FlaskClient, access_token: str):
    response = client.post(
        '/car',
        json={'color': 'roxo', 'model': 'sedan', 'owner_id': 1},
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 400


def test_create_car_with_invalid_model(client: FlaskClient, access_token: str):
    response = client.post(
        '/car',
        json={'color': 'azul', 'model': 'caminhonete', 'owner_id': 1},
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 400


def test_create_car_with_nonexistent_owner(
    client: FlaskClient, access_token: str
):
    response = client.post(
        '/car',
        json={'color': 'blue', 'model': 'sedan', 'owner_id': 999},
        headers={'Authorization': access_token},
        follow_redirects=True,
    )
    assert response.status_code == 404


def test_get_car_with_invalid_id(client: FlaskClient, access_token: str):
    response = client.get('/car/999', headers={'Authorization': access_token})
    assert response.status_code == 404


def test_delete_car_with_invalid_id(client: FlaskClient, access_token: str):
    response = client.delete(
        '/car/999', headers={'Authorization': access_token}
    )
    assert response.status_code == 404


def test_route_not_found_with_authentication(
    client: FlaskClient, access_token: str
):
    response = client.get(
        '/rota_inexistente', headers={'Authorization': access_token}
    )
    assert response.status_code == 404


def test_method_not_allowed_with_authentication(
    client: FlaskClient, access_token: str
):
    response = client.put('/car', headers={'Authorization': access_token})
    assert response.status_code == 404


def test_route_not_found_without_authentication(client: FlaskClient):
    response = client.get('/rota_inexistente')
    assert response.status_code == 400


def test_method_not_allowed_without_authentication(client: FlaskClient):
    response = client.put('/car')
    assert response.status_code == 400
