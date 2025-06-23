import os
import subprocess
import time
import psutil
from pathlib import Path
import pytest

VK_TEAMS_INSTALL_DIR = Path(os.getenv('LOCALAPPDATA')) / 'Programs' / 'VK Teams'
VK_TEAMS_EXECUTABLE = VK_TEAMS_INSTALL_DIR / 'vkteams.exe'
PROCESS_NAME = 'vkteams.exe'
WAIT_TIMEOUT = 30
STARTUP_TIMEOUT = 60

def is_process_running():
    return any(p.info['name'] == PROCESS_NAME for p in psutil.process_iter(['name']))

def terminate_process():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == PROCESS_NAME:
            proc.kill()
            time.sleep(2)

@pytest.fixture(scope="module")
def launch_application():
    if not VK_TEAMS_EXECUTABLE.exists():
        pytest.skip(f"VK Teams не установлен в {VK_TEAMS_INSTALL_DIR}")
    terminate_process()
    process = subprocess.Popen([str(VK_TEAMS_EXECUTABLE)])
    time.sleep(5)
    yield process
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

def test_installation_directory_exists():
    assert VK_TEAMS_INSTALL_DIR.exists(), f"Директория установки {VK_TEAMS_INSTALL_DIR} не найдена"

def test_executable_file_exists():
    assert VK_TEAMS_EXECUTABLE.exists(), f"Исполняемый файл {VK_TEAMS_EXECUTABLE.name} не найден"

def test_application_launch(launch_application):
    assert launch_application.poll() is None, "Приложение не запустилось"
    assert is_process_running(), f"Процесс {PROCESS_NAME} не обнаружен"

def test_process_memory_usage(launch_application):
    time.sleep(5)
    for proc in psutil.process_iter(['name', 'memory_info']):
        if proc.info['name'] == PROCESS_NAME:
            mem_usage = proc.info['memory_info'].rss / (1024 * 1024)
            assert mem_usage > 10, f"Подозрительно низкое использование памяти: {mem_usage:.2f} MB"
            return
    pytest.fail(f"Процесс {PROCESS_NAME} не найден для проверки памяти")

def test_multiple_instances():
    try:
        second_instance = subprocess.Popen(
            [str(VK_TEAMS_EXECUTABLE)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(5)
        assert second_instance.poll() is not None, "Удалось запустить вторую копию приложения"
        assert is_process_running(), "Основной процесс завершился после попытки запуска второй копии"
    finally:
        if 'second_instance' in locals() and second_instance.poll() is None:
            second_instance.terminate()

def test_automatic_startup():
    terminate_process()
    assert not is_process_running(), "Приложение уже запущено перед тестом"
    process = subprocess.Popen([str(VK_TEAMS_EXECUTABLE)])
    start_time = time.time()
    while (time.time() - start_time) < STARTUP_TIMEOUT:
        if is_process_running():
            break
        time.sleep(1)
    else:
        pytest.fail(f"Приложение не запустилось в течение {STARTUP_TIMEOUT} секунд")
    assert process.poll() is None, "Процесс приложения завершился после запуска"
    try:
        for proc in psutil.process_iter(['name', 'memory_info']):
            if proc.info['name'] == PROCESS_NAME:
                mem_usage = proc.info['memory_info'].rss / (1024 * 1024)
                assert mem_usage > 5, f"Слишком низкое использование памяти: {mem_usage:.2f} MB"
                break
        else:
            pytest.fail(f"Не удалось найти процесс {PROCESS_NAME} для проверки памяти")
        assert (time.time() - start_time) < STARTUP_TIMEOUT, "Приложение запустилось слишком долго"
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()