import allure
import pytest
import requests
from data import Urls
from helpers import Delivery

@allure.suite("Создание курьеров")
class TestCreateCourier:

    @allure.title('Успешное создание курьера с уникальным логином')
    def test_create_courier_correct_data_ok_true(self):
        payload = Delivery.generation_data_for_registration()
        response = requests.post(Urls.URL_courier_create, data=payload, verify=False)
        assert response.status_code == 201 and response.json().get('ok') is True, \
             f'Ошибка: получен код {response.status_code}, содержимое: {response.json()}'

    @allure.title('Создание двух одинаковых курьеров')
    def test_create_two_similar_couriers(self):
        payload = Delivery.generation_data_for_registration()
        requests.post(Urls.URL_courier_create, data=payload)
        response = requests.post(Urls.URL_courier_create, data=payload)
        assert response.status_code == 409 and response.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Создание курьера без поля: login')
    def test_create_courier_without_login(self):
        payload = Delivery.register_courier()  # Генерация данных для курьера
        del payload['login']  # Удаление поля login
        response = requests.post(Urls.URL_courier_create, data=payload)  # Запрос на создание курьера
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для создания учетной записи'

    @allure.title('Создание курьера без поля: password')
    def test_create_courier_without_password(self):
        payload = Delivery.register_courier()  # Генерация данных для курьера
        del payload['password']  # Удаление поля password
        response = requests.post(Urls.URL_courier_create, data=payload)  # Запрос на создание курьера
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для создания учетной записи'