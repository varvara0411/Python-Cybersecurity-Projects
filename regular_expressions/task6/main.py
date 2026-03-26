import re
import sys

# инициализируем счетчик для строк со словом "Failed"
failure_count = 0

# определяем слово (паттерн), которое ищем (с учетом регистра)
pattern = "Failed"

# читаем стандартный ввод строка за строкой
for line in sys.stdin:
    # в каждой строке ищем заданный паттерн
    # поиск чувствителен к регистру по умолчанию
    match = re.search(pattern, line)

    # если совпадение найдено (результат не None)
    if match is not None:
        # увеличиваем счетчик
        failure_count += 1

# после обработки всех строк выводим итоговый счетчик
print(failure_count)

# Альтернатива без re (для простого поиска подстроки):
# import sys

# failure_count = 0
# keyword = "Failed"

# for line in sys.stdin:
#     if keyword in line: # оператор 'in' тоже чувствителен к регистру
#         failure_count += 1

# print(failure_count)
