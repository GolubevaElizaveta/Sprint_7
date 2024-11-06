import pytest
import requests
import allure
from data import Urls

@allure.suite("Создание заказов")
class TestCreateOrder:

    @allure.title("Тест на создание заказа с различными цветами самоката")
    @allure.description("Проверка функциональности создания заказа с разными вариантами цветов: черный, серый, оба цвета и отсутствие указания цвета.")
    @pytest.mark.parametrize("color", [
        (["BLACK"], "Цвет: черный"),       # Тест с цветом черный
        (["GREY"], "Цвет: серый"),         # Тест с цветом серый
        (["BLACK", "GREY"], "Оба цвета"),  # Тест с обоими цветами
        ([], "Нет указанного цвета")       # Тест без указания цвета
    ])
    def test_create_order_with_colors(self, color):
        """Тестирование создания заказа с различными цветовыми параметрами"""
        color_value, color_desc = color

        payload = {
            "firstName": "Леонардо",
            "lastName": "ДиКаприо",
            "address": "Калифорния, улица Солнца, 101",
            "metroStation": 5,
            "phone": "+7 904 014 60 70",
            "rentTime": 7,
            "deliveryDate": "2024-11-15",
            "comment": "проверочка!"
        }

        # Добавляем цвет, если он указан
        if color_value:
            payload["color"] = color_value

        with allure.step(f"Отправка запроса на создание заказа с параметрами: {color_desc}"):
            response = requests.post(Urls.URL_orders_create, json=payload)

        with allure.step(f"Проверка успешного создания заказа с параметрами: {color_desc}"):
            assert response.status_code == 201 and "track" in response.json(), \
                f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}"