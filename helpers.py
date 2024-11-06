import allure
import requests
import random
import string
from data import Urls


class Delivery:
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    @allure.step('Генератор данных для регистрации курьера')
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
    @allure.step("Регистрация нового курьера")
    def register_courier():
        payload = Delivery.generation_data_for_registration()
        requests.post(Urls.URL_courier_create, data=payload)
        return payload

