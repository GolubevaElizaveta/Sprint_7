import allure
import pytest
import requests
from data import Urls
from helpers import Delivery

@allure.suite("Логин курьера в системе")
class TestAuthCourier:

    @allure.title('Успешная авторизация курьера')
    def test_courier_authorization(self):
        payload = Delivery.register_courier()  # Получаем данные для авторизации
        response = requests.post(Urls.URL_courier_login, json=payload)
        assert response.status_code == 200 and 'id' in response.json(), \
            f'Ошибка авторизации: {response.status_code}, ответ: {response.text}'

    @pytest.mark.parametrize('field', ['login', 'password'])
    @allure.title('Проверка авторизации с пустым значением поля')
    def test_auth_with_empty_field(self, field):
        payload = Delivery.register_courier()  # Получаем корректные данные
        payload[field] = ''  # Устанавливаем пустое значение
        response = requests.post(Urls.URL_courier_login, json=payload)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для входа', \
            f'Ошибка авторизации: {response.status_code}, ответ: {response.text}'

    @allure.title('Проверка авторизации с невалидными данными')
    @pytest.mark.parametrize("missing_credentials", [
        {'login': '', 'password': ''},
        {'login': 'plushki', 'password': ''},
        {'login': '', 'password': 'plushki'}
    ])
    def test_courier_login_with_missing_credentials(self, missing_credentials):
        response = requests.post(Urls.URL_courier_login, json=missing_credentials)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для входа', \
            f'Ошибка авторизации: {response.status_code}, ответ: {response.text}'

    @allure.title('Проверка авторизации с несуществующим курьером')
    def test_auth_with_nonexistent_courier(self):
        payload = Delivery.register_courier()  # Получаем данные нового курьера
        payload['login'] += '1'  # Изменяем логин на несуществующий
        response = requests.post(Urls.URL_courier_login, json=payload)
        assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена', \
            f'Ошибка авторизации: {response.status_code}, ответ: {response.text}'