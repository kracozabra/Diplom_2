import json
import allure
import pytest
import requests
import data
import helpers


class TestChangeUser:

    @allure.title('Проверка изменения пользователя с авторизацией')
    @pytest.mark.parametrize('field', ['email', 'name'])
    def test_change_authorized_user(self, field):
        token = helpers.register_new_user_and_return_token()
        updated_value = helpers.generate_random_login()
        payload = {field: updated_value}
        payload_json = json.dumps(payload)

        response = requests.patch(data.GET_CHANGE_USER_INFO, data=payload_json,
                                  headers={'Authorization': token, "Content-type": "application/json"})

        assert response.status_code == 200
        assert response.json()["user"][field] == updated_value

        helpers.delete_user_by_token(token)

    # Эти тесты не проходят из-за ошибки в API
    # После успешного запроса на разавторизацию токен продолжает работать
    @allure.title('Проверка изменения пользователя без авторизации')
    @pytest.mark.parametrize('field', ['email', 'name'])
    def test_change_non_authorized_user(self, field):
        response_registration = helpers.register_new_user_and_return_response()
        refresh_token = response_registration.json()['refreshToken']
        token = response_registration.json()['accessToken']
        helpers.logout_user_by_token(refresh_token)
        updated_value = helpers.generate_random_login()
        payload = {field: updated_value}
        payload_json = json.dumps(payload)

        response = requests.patch(data.GET_CHANGE_USER_INFO, data=payload_json,
                                  headers={'Authorization': token, "Content-type": "application/json"})

        assert response.status_code == 401
        assert response.json()["message"] == data.response_change_user_without_authorization

        helpers.delete_user_by_token(token)