import json
import allure
import pytest
import requests
import data
import helpers


class TestRegister:

    @allure.title('Проверка создания пользователя с корректными данными')
    def test_create_courier_with_correct_data(self):
        payload = helpers.generate_random_user_data()
        payload_json = json.dumps(payload)

        response = requests.post(data.REGISTER_USER_ENDPOINT, data=payload_json, headers=data.headers_json)

        assert response.status_code == 200
        assert response.json()['success'] == True

        helpers.delete_user_by_token(response.json()['accessToken'])

    @allure.title('Проверка создания пользователя с данными, которые уже есть у другого пользователя')
    def test_create_user_with_existing_data(self):
        payload = helpers.generate_random_user_data()
        payload_json = json.dumps(payload)

        response1 = requests.post(data.REGISTER_USER_ENDPOINT, data=payload_json, headers=data.headers_json)
        response2 = requests.post(data.REGISTER_USER_ENDPOINT, data=payload_json, headers=data.headers_json)

        assert response2.status_code == 403
        assert response2.json()['message'] == data.response_create_user_used_login

        helpers.delete_user_by_token(response1.json()['accessToken'])

    @allure.title('Проверка создания пользователя с пустым обязательным полем')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_create_user_with_empty_required_field(self, field):
        payload = helpers.generate_random_user_data()
        payload[field] = ''
        payload_json = json.dumps(payload)

        response = requests.post(data.REGISTER_USER_ENDPOINT, data=payload_json, headers=data.headers_json)

        assert response.status_code == 403
        assert response.json()['message'] == data.response_create_user_with_empty_field
