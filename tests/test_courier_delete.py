import allure
import requests
from data import Urls
from helpers import Delivery

@allure.suite("Удаление курьеров")
class TestCourierDeletion:

    @allure.title('Успешное удаление курьера')
    def test_successful_courier_deletion(self):
        # Сначала регистрируем курьера, чтобы получить ID
        payload = Delivery.register_courier()
        login_response = requests.post(Urls.URL_courier_login, json=payload)
        courier_id = login_response.json().get('id')

        # Выполняем запрос на удаление курьера
        delete_response = requests.delete(f"{Urls.URL_courier_delete}{courier_id}")

        # Проверяем успешное удаление
        assert delete_response.status_code == 200 and delete_response.json() == {"ok": True}, \
            f'Ошибка при удалении курьера: {delete_response.status_code}, ответ: {delete_response.text}'

    @allure.title('Ошибка при попытке удаления курьера без ID')
    def test_delete_courier_without_id(self):
        delete_response = requests.delete(Urls.URL_courier_delete)  # Запрос без ID

        # Проверяем ошибку 404
        assert delete_response.status_code == 404 and \
               delete_response.json()['message'] == "Not Found.", \
            f'Ошибка при удалении курьера: {delete_response.status_code}, ответ: {delete_response.text}'

    @allure.title('Ошибка при попытке удаления несуществующего курьера')
    def test_delete_nonexistent_courier(self):
        nonexistent_id = "1234567890"  # Не существующий ID
        delete_response = requests.delete(f"{Urls.URL_courier_delete}{nonexistent_id}")

        # Проверяем ошибку 404
        assert delete_response.status_code == 404 and \
               delete_response.json()['message'] == "Курьера с таким id нет.", \
            f'Ошибка при удалении курьера: {delete_response.status_code}, ответ: {delete_response.text}'