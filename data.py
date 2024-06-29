#URL-ы и ENDPOINT-ы
URL = 'https://stellarburgers.nomoreparties.site'
REGISTER_USER_ENDPOINT = URL + '/api/auth/register'
LOGIN_USER_ENDPOINT = URL + '/api/auth/login'
GET_CHANGE_USER_INFO = URL + '/api/auth/user'
CREATE_ORDER_ENDPOINT = URL + '/api/orders'
GET_ORDER_BY_USER = URL + '/api/orders'
GET_INGREDIENTS = URL + '/api/ingredients'
LOGOUT_USER_ENDPOINT = URL + '/api/auth/logout'

#Дополнитлельная информация для запросов
headers_json = {"Content-type": "application/json"}

#Тексты ответов API
response_create_user_success = '{"ok":true}'
response_create_user_with_empty_field = "Email, password and name are required fields"
response_create_user_used_login = "User already exists"
response_login_user_with_incorrect_data = "email or password are incorrect"
response_change_user_without_authorization = "You should be authorised"
response_create_order_without_ingredients = 'Ingredient ids must be provided'
response_create_order_with_incorrect_ingredients = 'One or more ids provided are incorrect'
