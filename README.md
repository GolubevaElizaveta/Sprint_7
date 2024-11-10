API-тесты для сервиса «Яндекс.Самокат»
Этот репозиторий содержит автотесты для проверки API сервиса "Яндекс.Самокат"

Использовалась документация:https://qa-scooter.praktikum-services.ru/docs/#api-Orders-AcceptOrder

Структура проекта
 - helpers для генерации данных
 - папка tests содержит тесты
 - data.py определены адреса сервиса 

Зависимости указаны в requirements.txt, установку можно выполнить: pip3 install -r requirements.txt

Как запустить тесты: pytest

Генерация отчетов
 - Чтобы сгенерировать Allure-отчёт pytest --alluredir=allure_results
 - Сформировать отчёт в формате веб-страницы allure serve allure_results

