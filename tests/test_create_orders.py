import json
import allure
import requests
import data
import helpers


class TestCreateOrders:

    @allure.title('Проверка создания заказа с авторизацией')
    def test_create_order_with_authorization(self):
        token = helpers.register_new_user_and_return_token()
        payload = {"ingredients": helpers.get_random_ingredients(5)}
        payload_json = json.dumps(payload)

        response = requests.post(data.CREATE_ORDER_ENDPOINT, data=payload_json,
                                 headers={'Authorization': token, "Content-type": "application/json"})

        assert response.status_code == 200
        assert response.json()["success"] == True


    # В документации не описано поведение на этот случай,
    # Поэтому считаю, что без автоизации должна возвращаться ошибка 401 (но возвращается 200)
    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_without_authorization(self):
        response_registration = helpers.register_new_user_and_return_response()
        refresh_token = response_registration.json()['refreshToken']
        token = response_registration.json()['accessToken']
        helpers.logout_user_by_token(refresh_token)
        payload = {"ingredients": helpers.get_random_ingredients(5)}
        payload_json = json.dumps(payload)

        response = requests.post(data.CREATE_ORDER_ENDPOINT, data=payload_json,
                                 headers={'Authorization': token, "Content-type": "application/json"})

        assert response.status_code == 401
        assert response.json()["success"] != True

    @allure.title('Проверка создания заказа без ингредиентов')
    def test_create_order_without_ingredients(self):
        token = helpers.register_new_user_and_return_token()
        payload = {"ingredients": []}
        payload_json = json.dumps(payload)

        response = requests.post(data.CREATE_ORDER_ENDPOINT, data=payload_json,
                                 headers={'Authorization': token, "Content-type": "application/json"})

        assert response.status_code == 400
        assert response.json()["message"] == data.response_create_order_without_ingredients

    @allure.title('Проверка создания заказа с некорректными значениями ингредиентов')
    def test_create_order_with_incorrect_ingredients(self):
        token = helpers.register_new_user_and_return_token()
        payload = {"ingredients": ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]}
        payload_json = json.dumps(payload)

        response = requests.post(data.CREATE_ORDER_ENDPOINT, data=payload_json,
                                 headers={'Authorization': token, "Content-type": "application/json"})

        assert response.status_code == 400
        assert response.json()["message"] == data.response_create_order_with_incorrect_ingredients
