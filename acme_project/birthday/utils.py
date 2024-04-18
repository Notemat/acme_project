from datetime import date


def calculate_birthday_countdown(birthday):
    """
    Возвращает количество дней до следующего Дня Рождения.

    Если оно сегодня, то возвращает 0.
    """
    today = date.today()
    this_year_birthday = get_birthday_for_year(birthday, today.year)
    if this_year_birthday < today:
        next_birthday = get_birthday_for_year(birthday, today.year + 1)
    else:
        next_birthday = this_year_birthday
    birthday_countdown = (next_birthday - today).days
    return birthday_countdown

def get_birthday_for_year(birthday, year):
    """
    Получает дату дня рождения для конкретного года.

    Если получает ошибку ValueError, значит год не високосный,
    а день рожения 29 февраля. В этом случае приравниваем др к 1 марта.
    """
    try:
        calculate_birthday = birthday.replace(year=year)
    except ValueError:
        calculate_birthday = date(year=year, month=3, day=1)
    return calculate_birthday
