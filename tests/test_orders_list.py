import allure
import requests
from data import Urls

@allure.suite("Получение списка заказа")
class TestOrderList:

    @allure.title('Проверяем список заказов')
    def test_check_status_order_list(self):
        response = requests.get(Urls.URL_orders_create)
        assert response.status_code == 200 and 'orders' in response.text