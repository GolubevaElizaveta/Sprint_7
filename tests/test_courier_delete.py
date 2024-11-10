import allure
import requests
from data import Urls
from helpers import Delivery


@allure.suite("Удаление курьеров")
class TestCourierDeletion:

    @allure.title('Успешное удаление курьера')
    def test_successful_courier_deletion(self):

        payload = Delivery.register_courier()  # Убедитесь, что этот метод работает корректно
        login_response = requests.post(Urls.URL_courier_login, json=payload)

        # Проверяем, что курьер успешно зарегистрирован и получаем его ID
        assert login_response.status_code == 200, f'Ошибка при логине курьера: {login_response.status_code}, ответ: {login_response.text}'
        courier_id = login_response.json().get('id')

        # Удаление курьера
        delete_response = requests.delete(f"{Urls.URL_courier_delete}{courier_id}")
        assert delete_response.status_code == 200, f'Ошибка при удалении курьера: {delete_response.status_code}, ответ: {delete_response.text}'

    @allure.title('Ошибка при попытке удаления курьера без ID')
    def test_delete_courier_without_id(self):
        delete_response = requests.delete(Urls.URL_courier_delete)
        assert delete_response.status_code == 404 and \
               delete_response.json()['message'] == "Not Found.", \
            f'Ошибка при удалении курьера: {delete_response.status_code}, ответ: {delete_response.text}'

    @allure.title('Ошибка при попытке удаления несуществующего курьера')
    def test_delete_nonexistent_courier(self):
        nonexistent_id = "1234567890"  # Не существующий ID
        delete_response = requests.delete(f"{Urls.URL_courier_delete}{nonexistent_id}")
        assert delete_response.status_code == 404 and delete_response.json()['message'] == "Курьера с таким id нет.", \
            f'Ошибка при удалении курьера: {delete_response.status_code}, ответ: {delete_response.text}'
