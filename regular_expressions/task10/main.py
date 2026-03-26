import re

try:
    # считываем строку из стандартного ввода
    input_string = input()

    # определяем паттерн для поиска:
    hex_pattern = r"[0-9a-fA-F]{10,}"

    # используем re.search() для поиска этого паттерна ГДЕ УГОДНО в строке
    match = re.search(hex_pattern, input_string)

    # проверяем результат поиска.
    result = bool(match)

    # выводим результат (True или False)
    print(result)

except EOFError:
    # Если возникла ошибка конца файла (вероятно, из-за пустого ввода),
    # то искомой последовательности точно нет.
    print(False)