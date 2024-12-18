import re

from datetime import datetime
from typing import Optional


async def validate_and_format_phone_number(phone_number: str) -> dict:
    # Убираем все лишние символы, кроме '+' в начале
    cleaned_number = re.sub(r'[^\d+]', '', phone_number)

    # Проверяем, что номер начинается с '+7', '7', или '8'
    if cleaned_number.startswith('+7'):
        cleaned_number = '7' + cleaned_number[2:]  # Убираем '+', оставляем '7'
    elif cleaned_number.startswith('8'):
        cleaned_number = '7' + cleaned_number[1:]  # Заменяем '8' на '7'
    elif not cleaned_number.startswith('7'):
        return {'valid': False, 'reason': 'Номер должен начинаться с +7, 7, или 8.'}

    # Проверяем длину номера (10 цифр после кода страны)
    if len(cleaned_number) != 11 or not cleaned_number.isdigit():
        return {'valid': False, 'reason': 'Неверное количество цифр в номере.'}

    # Форматируем номер в '+7 (XXX) XXX-XX-XX'
    formatted_number = f"+7 ({cleaned_number[1:4]}) {cleaned_number[4:7]}-{cleaned_number[7:9]}-{cleaned_number[9:]}"

    return {'valid': True, 'formatted': formatted_number}


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
        if ':' in date_str:
            # Формат с временем
            converted_str = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        else:
            # Формат только с датой
            converted_str = datetime.strptime(date_str, '%d.%m.%Y')
        return converted_str.date()
    except ValueError:
        return None
