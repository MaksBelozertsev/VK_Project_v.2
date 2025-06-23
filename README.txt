VK Project v.1

1. ПРЕДВАРИТЕЛЬНЫЕ ТРЕБОВАНИЯ
- Python 3.8 или новее
- Установленные пакеты: pytest, python-dotenv
- IDE PeCharm
- Miniconda

2. УСТАНОВКА
    1. Сделайте клон репозитори.
    2. Установите зависимости:
       conda env create -f env.yml
    3. Активируйте окружение:
       conda activate vk_tests

3. ЗАПУСК ТЕСТОВ
Основная команда:
    python run_tests.py

   Этот скрипт выполнит:
   - Установку (run_install.py)
   - Запуск тестов (run_test_report.py → тесты из tests/)
   - Удаление (run_uninstall.py)

Логика работы:
1. run_install.py
   - Устанавливает VK Teams

2. run_test_report.py
   - запускает тесты из папки tests
   - сохраняет отчет в папку reports в формате html

3. run_uninstall.py
   - Удаляет VK Teams


Тесты:

В папке tests/ находятся:
- test_install.py - проверка корректности установки

Отчеты:
В папке reports создаются отчеты о прохождении тестов в формате html
В папке log создаются отчеты о прохождении всего пути тестового сценария - установка ПО -> проведение тестов -> удаление ПО.