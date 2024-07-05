import json
import allure
import requests
import data
import helpers


class TestCreateOrders:

    @allure.title('Проверка создания заказа с авторизацией')
    def test_create_order_with_authorization(self, register_return_token_delete_user):
        token = register_return_token_delete_user
        payload = {"ingredients": helpers.get_random_ingredients(5)}
        payload_json = json.dumps(payload)
        headers_json = helpers.generate_headers_with_token(token)

        response = requests.post(data.CREATE_ORDER_ENDPOINT, data=payload_json, headers=headers_json)

        assert response.status_code == data.STATUS_200
        assert response.json()["success"] == True


    # В документации не описано поведение на этот случай,
    # Поэтому считаю, что без автоизации должна возвращаться ошибка 401 (но возвращается 200)
    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_without_authorization(self, register_return_response_delete_user):
        response_registration = register_return_response_delete_user
        refresh_token = response_registration.json()['refreshToken']
        token = response_registration.json()['accessToken']
        helpers.logout_user_by_token(refresh_token)
        payload = {"ingredients": helpers.get_random_ingredients(5)}
        payload_json = json.dumps(payload)
        headers_json = helpers.generate_headers_with_token(token)

        response = requests.post(data.CREATE_ORDER_ENDPOINT, data=payload_json, headers=headers_json)

        assert response.status_code == data.STATUS_401
        assert response.json()["success"] != True

    @allure.title('Проверка создания заказа без ингредиентов')
    def test_create_order_without_ingredients(self, register_return_token_delete_user):
        token = register_return_token_delete_user
        payload = {"ingredients": []}
        payload_json = json.dumps(payload)
        headers_json = helpers.generate_headers_with_token(token)

        response = requests.post(data.CREATE_ORDER_ENDPOINT, data=payload_json, headers=headers_json)

        assert response.status_code == data.STATUS_400
        assert response.json()["message"] == data.RESPONSE_CREATE_ORDER_WITHOUT_INGREDIENTS

    @allure.title('Проверка создания заказа с некорректными значениями ингредиентов')
    def test_create_order_with_incorrect_ingredients(self, register_return_token_delete_user):
        token = register_return_token_delete_user
        payload = data.INCORRECT_INGREDIENTS_PAYLOAD
        payload_json = json.dumps(payload)
        headers_json = helpers.generate_headers_with_token(token)

        response = requests.post(data.CREATE_ORDER_ENDPOINT, data=payload_json, headers=headers_json)

        assert response.status_code == data.STATUS_400
        assert response.json()["message"] == data.RESPONSE_CREATE_ORDER_WITH_INCORRECT_INGREDIENTS
