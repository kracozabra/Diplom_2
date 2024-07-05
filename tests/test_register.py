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

        response = requests.post(data.REGISTER_USER_ENDPOINT, data=payload_json, headers=data.HEADERS_JSON)

        assert response.status_code == data.STATUS_200
        assert response.json()['success'] == True

        helpers.delete_user_by_token(response.json()['accessToken'])

    @allure.title('Проверка создания пользователя с данными, которые уже есть у другого пользователя')
    def test_create_user_with_existing_data(self):
        payload = helpers.generate_random_user_data()
        payload_json = json.dumps(payload)

        response1 = requests.post(data.REGISTER_USER_ENDPOINT, data=payload_json, headers=data.HEADERS_JSON)
        response2 = requests.post(data.REGISTER_USER_ENDPOINT, data=payload_json, headers=data.HEADERS_JSON)

        assert response2.status_code == data.STATUS_403
        assert response2.json()['message'] == data.RESPONSE_CREATE_USER_USED_LOGIN

        helpers.delete_user_by_token(response1.json()['accessToken'])

    @allure.title('Проверка создания пользователя с пустым обязательным полем')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_create_user_with_empty_required_field(self, field):
        payload = helpers.generate_random_user_data()
        payload[field] = ''
        payload_json = json.dumps(payload)

        response = requests.post(data.REGISTER_USER_ENDPOINT, data=payload_json, headers=data.HEADERS_JSON)

        assert response.status_code == data.STATUS_403
        assert response.json()['message'] == data.RESPONSE_CREATE_USER_WITH_EMPTY_FIELD
