import os
import sys
import subprocess
import threading
from typing import Optional
from logger_config import get_logger

logger = get_logger(__name__, "run_check.log")


def input_with_timeout(prompt: str, timeout: int = 5) -> Optional[str]:
    """
    Промптить користувача для введення з обмеженням часу.

    Args:
        prompt (str): Повідомлення для користувача.
        timeout (int): Час очікування в секундах.

    Returns:
        Optional[str]: Введені дані або None у разі таймауту.
    """
    result = []

    def timed_input():
        result.append(input(prompt))

    thread = threading.Thread(target=timed_input)
    thread.start()
    thread.join(timeout)

    if result:
        return result[0].strip().lower()
    print("Час вийшов!")
    return None


def run_check(command: list[str]) -> bool:
    """
    Запускає перевірку та обробляє помилки.

    Args:
        command (list[str]): Команда для виконання.

    Returns:
        bool: True, якщо виконано без помилок, інакше False.
    """
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def run_linter_or_type_checks(file_name: str):
    """
    Запускає `mypy`, `pyright`, `pylint` у послідовності.
    Якщо тест провалюється, запитує користувача, чи продовжувати.

    Args:
        file_name (str): Файл для перевірки.
    """
    checkers = [("mypy", ["mypy", file_name]),
                ("pyright", ["pyright", file_name]),
                ("pylint", ["pylint", file_name])]

    for name, command in checkers:
        logger.info("Запускається %s...", name)
        if not run_check(command):
            logger.error("%s знайшов помилки у файлі %s.", name, file_name)
            response = input_with_timeout("Бажаєте продовжити наступний тест? (yes/y/1 для так, no/n/0 для ні): ", 5)
            if response not in {"yes", "y", "1"}:
                print("Перевірка зупинена.")
                return


def choose_file_and_run_checks():
    """
    Дозволяє користувачу вибрати Python-файл та запустити перевірки.
    """
    check_directory = os.getcwd()

    files = [f for f in os.listdir(check_directory) if f.endswith(".py")]
    if not files:
        logger.error("У директорії немає .py файлів.")
        sys.exit(1)

    print("Доступні файли:")
    for i, file in enumerate(files, 1):
        print(f"{i}: {file}")

    try:
        choice = int(input("Оберіть файл за номером: ")) - 1
        if choice < 0 or choice >= len(files):
            raise ValueError
    except ValueError:
        logger.error("Некоректний вибір.")
        sys.exit(1)

    run_linter_or_type_checks(files[choice])


def main():
    try:
        choose_file_and_run_checks()
    except KeyboardInterrupt:
        logger.error("Процес перервано користувачем.")
        sys.exit(1)


if __name__ == "__main__":
    main()
