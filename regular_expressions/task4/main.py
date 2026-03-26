import re

# считываем строку для проверки из стандартного ввода
input_string = input()

# определяем паттерн, который должен описывать ВСЮ строку:
#   \d{2} - ровно две цифры
#   :   - символ двоеточия
#   паттерн повторяется трижды для ЧЧ:ММ:СС
time_format_pattern = r"\d{2}:\d{2}:\d{2}"

# используем re.fullmatch() для проверки, соответствует ли ВСЯ строка паттерну
match = re.fullmatch(time_format_pattern, input_string)

# преобразуем результат в True (если вся строка совпала) или False (если нет)
is_valid = bool(match)

# выводим результат (True или False)
print(is_valid)

# ----- Альтернативное решение с использованием re.match() и якорей -----
# import re

# input_string = input()

# добавляем якоря ^ (начало строки) и $ (конец строки) к паттерну
# time_format_pattern_anchored = r"^\d{2}:\d{2}:\d{2}$"

# используем re.match(), который проверяет совпадение с начала строки
# match = re.match(time_format_pattern_anchored, input_string)

# is_valid = bool(match)
# print(is_valid)
# --------------------------------------------------------------------

