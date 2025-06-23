import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
import os
import locale


def setup_console_encoding():
    """Настройка кодировки консоли для корректного отображения символов"""
    try:
        # Для Windows
        if sys.platform == "win32":
            import win32api
            win32api.SetConsoleOutputCP(65001)  # UTF-8
            os.environ["PYTHONIOENCODING"] = "utf-8"

        # Принудительная установка UTF-8 для всех платформ
        if sys.version_info >= (3, 7):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        else:
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except Exception as e:
        print(f"Warning: Could not set console encoding: {str(e)}")


def log_message(message, log_file):
    """Логирование сообщений с обработкой Unicode"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        safe_message = message.encode('utf-8', errors='replace').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        safe_message = message.encode('ascii', errors='replace').decode('ascii')

    full_message = f"[{timestamp}] {safe_message}"

    try:
        print(full_message)
    except UnicodeEncodeError:
        print(full_message.encode('ascii', errors='replace').decode('ascii'))

    try:
        with open(log_file, 'a', encoding='utf-8', errors='replace') as f:
            f.write(full_message + "\n")
    except Exception as e:
        print(f"Ошибка записи в лог: {str(e)}")


def run_script(script_path, action_name, log_file):
    """Запуск скрипта с обработкой кодировок"""
    log_message(f"[Установка] {action_name}...", log_file)
    try:
        # Создаем окружение с UTF-8
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            errors='replace',
            env=env,
            text=True
        )

        # Очистка и нормализация вывода
        output = f"{result.stdout or ''}\n{result.stderr or ''}".strip()
        clean_output = output.encode('utf-8', errors='replace').decode('utf-8')

        log_message(f"Полный вывод:\n{clean_output}", log_file)

        if "test" in action_name.lower():
            return True, clean_output

        if result.returncode != 0:
            log_message(f"[Ошибка] {action_name} завершился с кодом {result.returncode}", log_file)
            return False, clean_output

        log_message(f"[Успех] {action_name} завершен успешно", log_file)
        return True, clean_output

    except Exception as e:
        error_msg = str(e).encode('utf-8', errors='replace').decode('utf-8')
        log_message(f"[Критическая ошибка] При {action_name.lower()}: {error_msg}", log_file)
        return False, error_msg


def main():
    setup_console_encoding()

    base_dir = Path("C:\\Users\\beloz\\PycharmProjects\\VK_project_v.2")
    install_script = base_dir / "run_install.py"
    report_script = base_dir / "run_test_report.py"
    uninstall_script = base_dir / "run_uninstall.py"

    log_dir = base_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    install_success, _ = run_script(install_script, "Установка приложения", log_file)
    if not install_success:
        log_message("❌ Прерывание: установка не удалась", log_file)
        sys.exit(1)

    log_message("⏳ Ожидание 60 секунд перед запуском отчета...", log_file)
    time.sleep(60)

    report_success, report_output = run_script(report_script, "Генерация отчета", log_file)
    if report_success:
        log_message("📊 Отчет успешно сгенерирован", log_file)
        log_message(f"Вывод скрипта отчета:\n{report_output}", log_file)
    else:
        log_message("❌ Ошибка при генерации отчета", log_file)

    log_message("🧹 Запуск удаления приложения...", log_file)
    uninstall_success, _ = run_script(uninstall_script, "Удаление приложения", log_file)

    log_message("\n=== FINAL REPORT ===", log_file)
    log_message(f"Установка: {'✅ Успешно' if install_success else '❌ Ошибка'}", log_file)
    log_message(f"Отчет: {'✅ Успешно' if report_success else '❌ Ошибка'}", log_file)
    log_message(f"Удаление: {'✅ Успешно' if uninstall_success else '❌ Ошибка'}", log_file)

    if install_success and report_success and uninstall_success:
        log_message("🎉 ВСЕ ОПЕРАЦИИ ВЫПОЛНЕНЫ УСПЕШНО", log_file)
        sys.exit(0)
    else:
        log_message("🔥 ОБНАРУЖЕНЫ ПРОБЛЕМЫ", log_file)
        sys.exit(1)


if __name__ == "__main__":
    main()