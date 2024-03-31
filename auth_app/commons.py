from django.utils import timezone
import datetime
from random import randrange


def default_pin_code() -> str:
    """Возвращет 6-значный пин-код, сгенерированный случайным образом"""
    return str(randrange(100000, 999999))


def default_date():
    """Текущая дата с учетом чалового пояса.
     Используется для подстановки даты по умолчанию"""
    return timezone.now()


def default_date_plus_five_min():
    """Текущая дата с учетом чалового пояса сдвинутая на 5 минут.
     Используется для подстановки даты по умолчанию"""
    return default_date() + datetime.timedelta(minutes=5)
