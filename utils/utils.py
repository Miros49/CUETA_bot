import re

from datetime import timedelta


def find_lolz_profile(text: str) -> str:
    lines = text.strip().split('\n')

    lolz_profile = None

    for line in lines:
        if line.startswith('Профиль Lolz:'):
            lolz_profile = line.split('Профиль Lolz:')[1].strip()
            break

    return lolz_profile


def find_referral_id(message: str) -> str | None:
    pattern = r"Приглашён пользователем: @\w+ \((\d+)\)"

    match = re.search(pattern, message)

    if match:
        return match.group(1)
    else:
        return None


def parse_duration(duration: str) -> timedelta | None:
    match = re.match(r"(\d+)([smhd])", duration)
    if not match:
        return None

    value, unit = int(match.group(1)), match.group(2)
    if unit == 's':
        return timedelta(seconds=value)
    elif unit == 'm':
        return timedelta(minutes=value)
    elif unit == 'h':
        return timedelta(hours=value)
    elif unit == 'd':
        return timedelta(days=value)
    return None


def parse_deposit(text: str):
    lines = text.strip().split('\n')

    amount = None
    worker = None

    for line in lines:
        if line.startswith('сумма:'):
            amount = float(line.split('сумма:')[1].strip())
        elif line.startswith('воркер:'):
            worker = line.split('воркер:')[1].strip()

    return amount, worker


async def get_percent(total_turnover: float) -> int:
    if total_turnover < 10000:
        return 50
    elif total_turnover < 60000:
        return 55
    elif total_turnover < 140000:
        return 60
    elif total_turnover < 240000:
        return 65
    return 70


async def get_limits(total_turnover: float) -> dict:
    if total_turnover < 10000:
        return {"proxy": 1, "numbers": 0}
    return {"proxy": 3, "numbers": 1}


async def parse_payout_info(message: str) -> dict:
    extracted_data = {}
    success = True

    wallet_match = re.search(r'👛\s(.*?):\s(.*)', message)
    if wallet_match:
        extracted_data['wallet_type'] = wallet_match.group(1)
        extracted_data['wallet'] = wallet_match.group(2)
    else:
        success = False

    amount_match = re.search(r'💵\sСумма:\s(.*?)\$', message)
    if amount_match:
        extracted_data['amount'] = float(amount_match.group(1))
    else:
        success = False

    user_match = re.search(r'👤\sВоркер:\s@(.+?)\s\((\d+)\)', message)
    if user_match:
        extracted_data['username'] = user_match.group(1)
        extracted_data['tg_id'] = int(user_match.group(2))
    else:
        success = False

    extracted_data["success"] = success

    return extracted_data
