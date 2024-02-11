import re

def validate_date(input_date):
    pattern = r'^(\d{8})$'  # Проверка на соответствие формату ГГГГММДД
    if re.match(pattern, input_date):
        print("Дата введена корректно")
    else:
        print("Неверный формат даты")