import os
import psutil
from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def vk_teams_path():
    """Путь к установленному приложению"""
    return Path(os.environ["LOCALAPPDATA"]) / "Programs" / "VK Teams"

def test_installation_dir_exists(vk_teams_path):
    """Проверка существования папки установки"""
    assert vk_teams_path.exists(), "Папка установки не найдена"

def test_executable_exists(vk_teams_path):
    """Проверка наличия исполняемого файла"""
    exe_path = vk_teams_path / "vkteams.exe"
    assert exe_path.exists(), "Исполняемый файл не найден"

def test_shortcut_exists():
    """Проверка ярлыка на рабочем столе"""
    desktop = Path(os.environ["USERPROFILE"]) / "Desktop"
    assert (desktop / "VK Teams.lnk").exists(), "Ярлык не создан"