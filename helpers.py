import json
import allure
import requests
import data
from faker import Faker


@allure.step('Генерируем случайные данные для создания пользователя')
def generate_random_user_data():
    fake = Faker(locale="ru_Ru")

    user_create_data = {
        "email": fake.email(),
        "password": fake.password(length=10),
        "name": fake.first_name()
    }
    return user_create_data


@allure.step('Генерируем случайный логин')
def generate_random_login():
    fake = Faker(locale="ru_RU")
    return fake.user_name()


@allure.step('Удаляем пользователя по его токену')
def delete_user_by_token(token):
    response = requests.delete(data.GET_CHANGE_USER_INFO, headers={'Authorization': token})
    print(response.json()['message'])


@allure.step('Создаем нового пользователя и получаем его логин и пароль')
def register_new_user_and_return_login_password():
    payload = generate_random_user_data()
    user_login_data = {}
    response = requests.post(data.REGISTER_USER_ENDPOINT, data=payload)
    if response.status_code == 200:
        user_login_data = {
            "email": payload['email'],
            "password": payload['password']
        }
    return user_login_data


@allure.step('Создаем нового пользователя и получаем его токен')
def register_new_user_and_return_token():
    payload = generate_random_user_data()
    response = requests.post(data.REGISTER_USER_ENDPOINT, data=payload)
    if response.status_code == 200:
        token = response.json()['accessToken']
    return token


@allure.step('Создаем нового пользователя и получаем ответ полностью')
def register_new_user_and_return_response():
    payload = generate_random_user_data()
    response = requests.post(data.REGISTER_USER_ENDPOINT, data=payload)
    if response.status_code == 200:
        return response


@allure.step('Разлогиниваем пользователя')
def logout_user_by_token(refresh_token):
    payload = {"token": refresh_token}
    payload_json = json.dumps(payload)
    requests.post(data.LOGOUT_USER_ENDPOINT, data=payload_json, headers=data.headers_json)


@allure.step('Создаем список существующих ингредиентов')
def get_random_ingredients(number):
    ingredients = []
    response = requests.get(data.GET_INGREDIENTS)
    for i in range(number):
        ingredients.append(response.json()['data'][i]['_id'])
    return ingredients


@allure.step('Создаем заказ по токену и возвращаем его id')
def create_order(token):
    payload = {"ingredients": get_random_ingredients(5)}
    payload_json = json.dumps(payload)
    response = requests.post(data.CREATE_ORDER_ENDPOINT, data=payload_json,
                             headers={'Authorization': token, "Content-type": "application/json"})
    return response.json()["order"]["_id"]
