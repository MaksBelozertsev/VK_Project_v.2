import subprocess
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

SCRIPTS_DIR = Path(__file__).parent
INSTALL_SCRIPT = SCRIPTS_DIR / "run_install.py"
UNINSTALL_SCRIPT = SCRIPTS_DIR / "run_uninstall.py"
TESTS_DIR = SCRIPTS_DIR / "tests"


def main():
    try:
        # 1. Установка
        logging.info("Запуск установки...")
        subprocess.run(["python", str(INSTALL_SCRIPT)], check=True)

        # 2. Тестирование
        logging.info("Запуск тестов...")
        subprocess.run(["pytest", str(TESTS_DIR)], check=True)

        # 3. Удаление
        logging.info("Запуск удаления...")
        subprocess.run(["python", str(UNINSTALL_SCRIPT)], check=True)

        logging.info("Все операции завершены успешно!")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка выполнения: {e}")
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")


if __name__ == "__main__":
    main()