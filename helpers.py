import requests
import random
import string
import allure
from data import Urls
import pytest


class Delivery:
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def generation_data_for_registration():
        login = Delivery.generate_random_string(10)
        password = Delivery.generate_random_string(10)
        first_name = Delivery.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return payload

    @staticmethod
    def register_courier():
        payload = Delivery.generation_data_for_registration()
        response = requests.post(Urls.URL_courier_create, json=payload)
        if response.status_code == 201:
            return payload  # Возвращаем данные для авторизации
        else:
            raise Exception(f'Ошибка при регистрации курьера: {response.status_code}, ответ: {response.json()}')


@pytest.fixture(scope="function")
def courier():
    # Генерация данных для регистрации курьера
    payload = Delivery.generation_data_for_registration()

    # Регистрация курьера
    response = requests.post(Urls.URL_courier_create, json=payload, verify=False)
    assert response.status_code == 201, f'Ошибка при регистрации курьера: {response.status_code}, ответ: {response.json()}'

    # Получаем ID курьера для удаления
    courier_id = response.json().get('id')
    yield courier_id  # Возвращаем ID курьера для использования в тестах

    # Удаление курьера после теста
    delete_response = requests.delete(f"{Urls.URL_courier_delete}{courier_id}", verify=False)
    assert delete_response.status_code == 200, f'Ошибка при удалении курьера: {delete_response.status_code}, ответ: {delete_response.json()}'
