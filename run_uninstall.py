import os
import shutil
import subprocess
import time
from pathlib import Path

APP_NAME = "VK Teams"
INSTALL_DIR = Path(os.environ["LOCALAPPDATA"]) / "Programs" / "VK Teams"
PROCESS_NAMES = ["vk-teams.exe", "VK Teams.exe", "VKTeamsUpdater.exe"]
LEFTOVER_LOCATIONS = [
    Path(os.environ["APPDATA"]) / "VK Teams",
    Path(os.environ["LOCALAPPDATA"]) / "VK Teams",
    Path(os.environ["TEMP"]) / "VK Teams",
    Path(os.environ["PUBLIC"]) / "Desktop" / "VK Teams.lnk",
    Path(os.environ["USERPROFILE"]) / "Desktop" / "VK Teams.lnk",
    Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "VK Teams.lnk",
    Path(os.environ["LOCALAPPDATA"]) / "Temp" / "VK Teams",
    Path(os.environ["LOCALAPPDATA"]) / "SquirrelTemp",
]

def kill_processes():
    print(f"🔴 Завершение процессов {APP_NAME}...")
    for proc in PROCESS_NAMES:
        for _ in range(3):
            try:
                subprocess.run(
                    ["taskkill", "/f", "/im", proc],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
                print(f"✓ Процесс {proc} завершен")
                break
            except subprocess.CalledProcessError:
                time.sleep(1)
        else:
            print(f"⚠ Не удалось завершить {proc}")

def remove_installation_dir():
    print(f"Удаление основной папки: {INSTALL_DIR}")
    for attempt in range(3):
        try:
            if INSTALL_DIR.exists():
                shutil.rmtree(INSTALL_DIR, ignore_errors=True)
                print("✓ Папка приложения удалена")
                return True
            else:
                print("Папка приложения не найдена")
                return False
        except Exception as e:
            print(f"⚠ Ошибка (попытка {attempt + 1}): {e}")
            time.sleep(2)
    return False

def clean_leftovers():
    print("Очистка остаточных файлов...")
    for location in LEFTOVER_LOCATIONS:
        try:
            if location.exists():
                if location.is_file():
                    location.unlink()
                    print(f"✓ Удален файл: {location}")
                else:
                    shutil.rmtree(location, ignore_errors=True)
                    print(f"✓ Удалена папка: {location}")
        except Exception as e:
            print(f"Ошибка при удалении {location}: {e}")

def verify_uninstallation():
    remaining = []
    all_locations = [INSTALL_DIR] + LEFTOVER_LOCATIONS
    for location in all_locations:
        if location.exists():
            remaining.append(str(location))
    if remaining:
        print("\n Оставшиеся элементы:")
        for item in remaining:
            print(f"• {item}")
        return False
    return True

def main():
    print(f"\n{'=' * 50}")
    print(f" Начало удаления {APP_NAME}".center(50))
    print(f"{'=' * 50}\n")
    kill_processes()
    remove_installation_dir()
    clean_leftovers()
    print(f"\n{'=' * 50}")
    if verify_uninstallation():
        print(f" {APP_NAME} успешно удалён!".center(50))
    else:
        print(f" Удаление завершено с ошибками".center(50))
    print(f"{'=' * 50}\n")

if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        print("Требуются права администратора! Запустите скрипт от имени администратора.")