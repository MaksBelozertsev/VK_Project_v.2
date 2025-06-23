import pytest
import datetime
import os
from pathlib import Path


def generate_report_path():
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return reports_dir / f"report_{timestamp}.html"


if __name__ == "__main__":
    args = [
        "--emoji",
        "-v",
        "--html", str(generate_report_path()),
        "--self-contained-html",
        "--color=yes",
        "--durations=5",
    ]

    os.environ["PYTEST_ADDOPTS"] = ""

    exit_code = pytest.main(args)

    if exit_code == 0:
        print("\n🎉 Все тесты прошли успешно!")
    else:
        print("\n❌ Обнаружены ошибки в тестах!")

    print(f"\n📊 Отчёт сохранён в: {generate_report_path()}")