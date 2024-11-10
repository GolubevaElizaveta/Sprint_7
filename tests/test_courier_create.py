import allure
import pytest
import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from data import Urls
from helpers import Delivery

# Игнорировать предупреждения о незащищенных запросах
warnings.simplefilter('ignore', InsecureRequestWarning)


@allure.suite("Создание курьеров")
class TestCreateCourier:

    @allure.title('Успешное создание курьера с уникальным логином')
    def test_create_courier_correct_data_ok_true(self):
        payload = Delivery.generation_data_for_registration()
        response = requests.post(Urls.URL_courier_create, json=payload)
        if response.status_code == 201 and response.json().get('ok') is True:
            # Получаем ID курьера для удаления
            courier_id = response.json().get('id')

            # Удаление курьера
            if courier_id:
                delete_response = requests.delete(f"{Urls.URL_courier_delete}{courier_id}", verify=False)
                if delete_response.status_code != 200:
                    print(
                        f'Ошибка при удалении курьера: {delete_response.status_code}, ответ: {delete_response.json()}')
            else:
                print("ID курьера не получен")
        else:
            print(f'Ошибка: получен код {response.status_code}, содержимое: {response.json()}')

    @allure.title('Создание двух одинаковых курьеров')
    def test_create_two_similar_couriers(self):
        payload = Delivery.generation_data_for_registration()
        requests.post(Urls.URL_courier_create, json=payload)  # Регистрация первого курьера
        response = requests.post(Urls.URL_courier_create, json=payload)  # Попытка регистрации второго
        assert response.status_code == 409 and response.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Создание курьера без поля: login')
    def test_create_courier_without_login(self):
        payload = Delivery.generation_data_for_registration()  # Генерация данных для курьера
        del payload['login']  # Удаление поля login
        response = requests.post(Urls.URL_courier_create, json=payload)  # Запрос на создание курьера
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для создания учетной записи'

    @allure.title('Создание курьера без поля: password')
    def test_create_courier_without_password(self):
        payload = Delivery.generation_data_for_registration()  # Генерация данных для курьера
        del payload['password']  # Удаление поля password
        response = requests.post(Urls.URL_courier_create, json=payload)  # Запрос на создание курьера
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для создания учетной записи'