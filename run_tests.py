import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
import os


def log_message(message, log_file):
    """Записывает сообщение в лог и выводит в консоль"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(full_message + "\n")


def run_script(script_path, action_name, log_file):
    """Запускает указанный скрипт с обработкой ошибок"""
    log_message(f"🔧 {action_name}...", log_file)
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=False,  # Отключаем автоматическую проверку кода возврата
            text=True,
            capture_output=True,
            encoding='utf-8'
        )

        # Всегда логируем полный вывод
        log_message(f"Полный вывод:\n{result.stdout}\n{result.stderr}", log_file)

        # Для тестов анализируем вывод независимо от кода возврата
        if "test" in action_name.lower():
            return True, result.stdout

        # Для других скриптов проверяем код возврата
        if result.returncode != 0:
            log_message(f"❌ {action_name} завершился с кодом {result.returncode}", log_file)
            return False, result.stderr

        log_message(f"✅ {action_name} успешно завершен", log_file)
        return True, result.stdout
    except Exception as e:
        log_message(f"❌ Неожиданная ошибка при {action_name.lower()}: {str(e)}", log_file)
        return False, str(e)


def main():
    # Настройка путей
    base_dir = Path("C:\\Users\\beloz\\PycharmProjects\\VK_project_v.2")
    install_script = base_dir / "run_install.py"
    report_script = base_dir / "run_test_report.py"  # Скрипт для генерации отчета
    uninstall_script = base_dir / "run_uninstall.py"

    # Создаем лог-файл
    log_dir = base_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    # 1. Установка приложения
    install_success, _ = run_script(install_script, "Установка приложения", log_file)
    if not install_success:
        log_message("❌ Прерывание: установка не удалась", log_file)
        sys.exit(1)

    # 2. Ожидание перед запуском отчета
    log_message("⏳ Ожидание 60 секунд перед запуском отчета...", log_file)
    time.sleep(60)

    # 3. Запуск скрипта отчета
    report_success, report_output = run_script(report_script, "Генерация отчета", log_file)

    if report_success:
        log_message("📊 Отчет успешно сгенерирован", log_file)
        log_message(f"Вывод скрипта отчета:\n{report_output}", log_file)
    else:
        log_message("❌ Ошибка при генерации отчета", log_file)

    # 4. Удаление приложения
    log_message("🧹 Запуск удаления приложения...", log_file)
    uninstall_success, _ = run_script(uninstall_script, "Удаление приложения", log_file)

    # 5. Итоговый отчет
    log_message("\n=== FINAL REPORT ===", log_file)
    log_message(f"Установка: {'Успешно' if install_success else 'Ошибка'}", log_file)
    log_message(f"Отчет: {'Успешно' if report_success else 'Ошибка'}", log_file)
    log_message(f"Удаление: {'Успешно' if uninstall_success else 'Ошибка'}", log_file)

    if install_success and report_success and uninstall_success:
        log_message("🎉 ВСЕ ОПЕРАЦИИ ВЫПОЛНЕНЫ УСПЕШНО", log_file)
        sys.exit(0)
    else:
        log_message("🔥 ОБНАРУЖЕНЫ ПРОБЛЕМЫ", log_file)
        sys.exit(1)


if __name__ == "__main__":
    main()