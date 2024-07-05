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


@allure.step('Генерируем headers с авторизацией')
def generate_headers_with_token(token):
    headers_with_token = {
        "Authorization": token,
        "Content-type": "application/json"
    }
    return headers_with_token


@allure.step('Разлогиниваем пользователя')
def logout_user_by_token(refresh_token):
    payload = {"token": refresh_token}
    payload_json = json.dumps(payload)
    requests.post(data.LOGOUT_USER_ENDPOINT, data=payload_json, headers=data.HEADERS_JSON)


@allure.step('Удаляем пользователя по его токену')
def delete_user_by_token(token):
    response = requests.delete(data.GET_CHANGE_USER_INFO, headers={'Authorization': token})


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
