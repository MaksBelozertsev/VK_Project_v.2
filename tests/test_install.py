import os
import subprocess
import time
import psutil
from pathlib import Path
import pytest

# Конфигурация тестов
VK_TEAMS_INSTALL_DIR = Path(os.getenv('LOCALAPPDATA')) / 'Programs' / 'VK Teams'
VK_TEAMS_EXECUTABLE = VK_TEAMS_INSTALL_DIR / 'vkteams.exe'
PROCESS_NAME = 'vkteams.exe'
WAIT_TIMEOUT = 30  # секунд на запуск приложения


@pytest.fixture(scope="module")
def launch_application():
    """Фикстура для запуска и завершения приложения"""
    if not VK_TEAMS_EXECUTABLE.exists():
        pytest.skip(f"VK Teams не установлен в {VK_TEAMS_INSTALL_DIR}")

    # Завершаем процесс, если уже запущен
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == PROCESS_NAME:
            proc.kill()
            time.sleep(2)

    # Запускаем приложение
    process = subprocess.Popen([str(VK_TEAMS_EXECUTABLE)])
    time.sleep(5)  # Даем время на запуск

    yield process

    # Завершаем процесс после тестов
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


def test_installation_directory_exists():
    """Проверяем, что директория установки существует"""
    assert VK_TEAMS_INSTALL_DIR.exists(), \
        f"Директория установки {VK_TEAMS_INSTALL_DIR} не найдена"


def test_executable_file_exists():
    """Проверяем наличие исполняемого файла"""
    assert VK_TEAMS_EXECUTABLE.exists(), \
        f"Исполняемый файл {VK_TEAMS_EXECUTABLE.name} не найден"


def test_application_launch(launch_application):
    """Проверяем, что приложение запускается"""
    # Проверяем, что процесс запущен
    assert launch_application.poll() is None, "Приложение не запустилось"

    # Проверяем наличие процесса в системе
    process_running = any(p.info['name'] == PROCESS_NAME
                          for p in psutil.process_iter(['name']))
    assert process_running, f"Процесс {PROCESS_NAME} не обнаружен"


def test_process_memory_usage(launch_application):
    """Проверяем, что приложение использует память (признак работы)"""
    time.sleep(5)  # Даем время на инициализацию

    for proc in psutil.process_iter(['name', 'memory_info']):
        if proc.info['name'] == PROCESS_NAME:
            mem_usage = proc.info['memory_info'].rss / (1024 * 1024)  # в MB
            assert mem_usage > 10, f"Подозрительно низкое использование памяти: {mem_usage:.2f} MB"
            return

    pytest.fail(f"Процесс {PROCESS_NAME} не найден для проверки памяти")


def test_multiple_instances():
    """Проверяем, что нельзя запустить вторую копию приложения"""
    try:
        # Пытаемся запустить вторую копию
        second_instance = subprocess.Popen(
            [str(VK_TEAMS_EXECUTABLE)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(5)

        # Проверяем, что вторая копия завершилась
        assert second_instance.poll() is not None, \
            "Удалось запустить вторую копию приложения"

        # Проверяем, что основной процесс все еще работает
        assert any(p.info['name'] == PROCESS_NAME
                   for p in psutil.process_iter(['name'])), \
            "Основной процесс завершился после попытки запуска второй копии"
    finally:
        # На всякий случай завершаем вторую копию
        if 'second_instance' in locals() and second_instance.poll() is None:
            second_instance.terminate()