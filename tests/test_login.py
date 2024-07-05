import json
import allure
import requests
import data
import helpers


class TestLogin:

    @allure.title('Проверка авторизации пользователя с существующим логином')
    def test_login_existing_user(self):
        payload = helpers.register_new_user_and_return_login_password()
        payload_json = json.dumps(payload)
        response = requests.post(data.LOGIN_USER_ENDPOINT, data=payload_json, headers=data.HEADERS_JSON)

        assert response.status_code == data.STATUS_200
        assert response.json()['success'] == True

        helpers.delete_user_by_token(response.json()['accessToken'])

    @allure.title('Проверка авторизации пользователя с несуществующим логином')
    def test_login_with_not_existing_login(self):
        payload = helpers.register_new_user_and_return_login_password()
        payload_json = json.dumps(payload)
        token = requests.post(data.LOGIN_USER_ENDPOINT, data=payload_json, headers=data.HEADERS_JSON).json()['accessToken']
        payload['email'] += '_not_exist'
        payload_json = json.dumps(payload)

        response = requests.post(data.LOGIN_USER_ENDPOINT, data=payload_json, headers=data.HEADERS_JSON)

        assert response.status_code == data.STATUS_401
        assert response.json()['message'] == data.RESPONSE_LOGIN_USER_WITH_INCORRECT_DATA

        helpers.delete_user_by_token(token)
