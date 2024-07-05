# Помогает корректно выводить символы кириллицы в консоли PyCharm
import pytest
import requests

import data
import helpers


def pytest_make_parametrize_id(config, val):
    return repr(val)


@pytest.fixture
def register_return_login_password_delete_user():
    payload = helpers.generate_random_user_data()
    user_login_data = {}
    response = requests.post(data.REGISTER_USER_ENDPOINT, data=payload)
    if response.status_code == 200:
        user_login_data = {
            "email": payload['email'],
            "password": payload['password']
        }
    token = response.json()['accessToken']
    yield user_login_data
    helpers.delete_user_by_token(token)


@pytest.fixture
def register_return_token_delete_user():
    payload = helpers.generate_random_user_data()
    response = requests.post(data.REGISTER_USER_ENDPOINT, data=payload)
    if response.status_code == 200:
        token = response.json()['accessToken']
    yield token
    helpers.delete_user_by_token(token)


@pytest.fixture
def register_return_response_delete_user():
    payload = helpers.generate_random_user_data()
    response = requests.post(data.REGISTER_USER_ENDPOINT, data=payload)
    if response.status_code == 200:
        yield response
    token = response.json()['accessToken']
    helpers.delete_user_by_token(token)
