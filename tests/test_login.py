import json
import allure
import requests
import data


class TestLogin:

    @allure.title('Проверка авторизации пользователя с существующим логином')
    def test_login_existing_user(self, register_return_login_password_delete_user):
        payload_json = json.dumps(register_return_login_password_delete_user)
        response = requests.post(data.LOGIN_USER_ENDPOINT, data=payload_json, headers=data.HEADERS_JSON)

        assert response.status_code == data.STATUS_200
        assert response.json()['success'] == True

    @allure.title('Проверка авторизации пользователя с несуществующим логином')
    def test_login_with_not_existing_login(self, register_return_login_password_delete_user):
        payload = register_return_login_password_delete_user
        payload['email'] += '_not_exist'
        payload_json = json.dumps(payload)

        response = requests.post(data.LOGIN_USER_ENDPOINT, data=payload_json, headers=data.HEADERS_JSON)

        assert response.status_code == data.STATUS_401
        assert response.json()['message'] == data.RESPONSE_LOGIN_USER_WITH_INCORRECT_DATA
