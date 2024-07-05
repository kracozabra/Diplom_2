#URL-ы и ENDPOINT-ы
URL = 'https://stellarburgers.nomoreparties.site'
REGISTER_USER_ENDPOINT = URL + '/api/auth/register'
LOGIN_USER_ENDPOINT = URL + '/api/auth/login'
GET_CHANGE_USER_INFO = URL + '/api/auth/user'
CREATE_ORDER_ENDPOINT = URL + '/api/orders'
GET_ORDER_BY_USER = URL + '/api/orders'
GET_INGREDIENTS = URL + '/api/ingredients'
LOGOUT_USER_ENDPOINT = URL + '/api/auth/logout'

#Дополнительная информация для запросов
HEADERS_JSON = {"Content-type": "application/json"}

#Коды ответов API
STATUS_200 = 200
STATUS_400 = 400
STATUS_401 = 401
STATUS_403 = 403

#Тексты ответов API
RESPONSE_CREATE_USER_SUCCESS = '{"ok":true}'
RESPONSE_CREATE_USER_WITH_EMPTY_FIELD = "Email, password and name are required fields"
RESPONSE_CREATE_USER_USED_LOGIN = "User already exists"
RESPONSE_LOGIN_USER_WITH_INCORRECT_DATA = "email or password are incorrect"
RESPONSE_CHANGE_USER_WITHOUT_AUTHORIZATION = "You should be authorised"
RESPONSE_CREATE_ORDER_WITHOUT_INGREDIENTS = 'Ingredient ids must be provided'
RESPONSE_CREATE_ORDER_WITH_INCORRECT_INGREDIENTS = 'One or more ids provided are incorrect'

#Данные для тестов
INCORRECT_INGREDIENTS = ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]
INCORRECT_INGREDIENTS_PAYLOAD = {"ingredients": INCORRECT_INGREDIENTS}
