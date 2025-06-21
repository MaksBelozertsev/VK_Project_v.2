import subprocess
import time
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError

# Путь к установщику
INSTALLER_PATH = r"C:\Users\beloz\Desktop\vkteamssetup.exe"


def automate_installation():
    print("🚀 Запуск установщика...")
    subprocess.Popen(INSTALLER_PATH)

    try:
        # Ждем появления окна (максимум 30 секунд)
        print("🔍 Поиск окна установки...")
        app = Application(backend="uia").connect(title_re=".*VK Teams.*", timeout=30)

        # Выводим информацию об окне для отладки
        main_window = app.window()
        print("ℹ️ Найдено окно:", main_window.window_text())
        main_window.print_control_identifiers()  # Выводим все элементы окна

        # Нажимаем кнопку "Установить"
        print("🖱️ Нажимаем кнопку 'Установить'...")
        install_button = main_window.child_window(
            title="Установить",
            control_type="Button"
        )
        install_button.click()

        print("⏳ Ожидаем завершения установки...")
        time.sleep(10)  # Даем время на установку

    except ElementNotFoundError:
        print("❌ Окно установки не найдено!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        print("✅ Процесс завершен")


if __name__ == "__main__":
    automate_installation()