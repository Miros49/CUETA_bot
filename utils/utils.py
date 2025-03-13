import re

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from datetime import datetime, date
from typing import Optional

from core import config, storage


async def validate_and_format_phone_number(phone_number: str) -> dict:
    # Убираем все лишние символы, кроме '+' в начале
    cleaned_number = re.sub(r"[^\d+]", "", phone_number)

    # Проверяем, что номер начинается с '+7', '7', или '8'
    if cleaned_number.startswith("+7"):
        cleaned_number = "7" + cleaned_number[2:]  # Убираем '+', оставляем '7'
    elif cleaned_number.startswith("8"):
        cleaned_number = "7" + cleaned_number[1:]  # Заменяем '8' на '7'
    elif not cleaned_number.startswith("7"):
        return {"valid": False, "reason": "Номер должен начинаться с +7, 7, или 8"}

    # Проверяем длину номера (10 цифр после кода страны)
    if len(cleaned_number) != 11 or not cleaned_number.isdigit():
        return {"valid": False, "reason": "Неверное количество цифр в номере"}

    # Форматируем номер в '+7 (XXX) XXX-XX-XX'
    formatted_number = f"+7 ({cleaned_number[1:4]}) {cleaned_number[4:7]}-{cleaned_number[7:9]}-{cleaned_number[9:]}"

    return {"valid": True, "formatted": formatted_number}


async def convert_string_to_date(date_str: str) -> Optional[datetime.date]:
    """
    Преобразует строку даты в объект datetime.date.
    Поддерживает форматы:
    - DD.MM.YYYY
    - DD.MM.YYYY HH:MM

    Args:
        date_str (str): Строка с датой или датой и временем.

    Returns:
        Optional[datetime.date]: Объект даты, если преобразование успешно, иначе None.
    """

    try:
        if ":" in date_str:
            # Формат с временем
            converted_str = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
        else:
            # Формат только с датой
            converted_str = datetime.strptime(date_str, "%d.%m.%Y")
        return converted_str.date()
    except ValueError:
        return None


def validate_date_of_birth(date_of_birth: str) -> dict:
    # Проверяем формат по длине
    if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", date_of_birth):
        return {
            "valid": False,
            "reason": "Введите дату своего рождения в формате ДД.ММ.ГГГГ:",
        }

    try:
        datetime.strptime(date_of_birth, "%d.%m.%Y")  # проверка формата
    except ValueError:
        return {
            "valid": False,
            "reason": "Введите дату своего рождения в формате ДД.ММ.ГГГГ:",
        }

    return {"valid": True}


def convert_date(us_date: date | str) -> str:
    """Конвертирует дату из формата YYYY-MM-DD в формат DD.MM.YYYY."""
    if isinstance(us_date, date):
        us_date = us_date.strftime("%Y-%m-%d")

    try:
        year, month, day = us_date.split("-")
        return f"{day}.{month}.{year}"
    except ValueError:
        raise ValueError(
            "Некорректный формат даты. Используйте YYYY-MM-DD или объект date."
        )


def is_user_adult(date_of_birth: date) -> bool:
    """
    Проверяет, исполнилось ли пользователю 18 лет.
    :param date_of_birth: Дата рождения пользователя.
    :return: True, если пользователю есть 18 лет, иначе False.
    """
    today = date.today()
    age = (
        today.year
        - date_of_birth.year
        - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    )
    return age >= 18


def get_user_state(user_id: str | int):
    return FSMContext(
        storage,
        StorageKey(
            bot_id=int(config.tg_bot.token.split(":")[0]),
            chat_id=user_id,
            user_id=user_id,
        ),
    )
