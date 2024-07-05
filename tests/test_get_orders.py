import allure
import requests
import data
import helpers


class TestGetOrders:

    @allure.title('Проверка получения заказов авторизованного пользователя')
    def test_get_order_with_authorization(self, register_return_token_delete_user):
        token = register_return_token_delete_user
        order_id = helpers.create_order(token)
        headers_json = helpers.generate_headers_with_token(token)

        response = requests.get(data.GET_ORDER_BY_USER, headers=headers_json)
        assert response.status_code == data.STATUS_200
        assert response.json()["orders"][0]["_id"] == order_id

    # Эти тесты не проходят из-за ошибки в API
    # После успешного запроса на разавторизацию токен продолжает работать
    @allure.title('Проверка получения заказов неавторизованного пользователя')
    def test_get_order_without_authorization(self, register_return_response_delete_user):
        response_registration = register_return_response_delete_user
        refresh_token = response_registration.json()['refreshToken']
        token = response_registration.json()['accessToken']
        helpers.create_order(token)
        headers_json = helpers.generate_headers_with_token(token)
        helpers.logout_user_by_token(refresh_token)

        response = requests.get(data.GET_ORDER_BY_USER, headers=headers_json)
        assert response.status_code == data.STATUS_401
        assert response.json()["orders"] is None
