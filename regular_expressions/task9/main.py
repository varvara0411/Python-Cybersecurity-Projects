import re

# считываем исходную строку лога из стандартного ввода
original_line = input()

# определяем упрощенный паттерн для поиска IPv4-адреса
ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

# определяем строку, на которую будем заменять найденный IP
replacement_string = "REDACTED"

# используем re.sub() для замены:
#   - ищем ip_pattern
#   - заменяем на replacement_string
#   - в строке original_line
#   - count=1 означает "заменить только первое найденное вхождение"
modified_line = re.sub(ip_pattern, replacement_string, original_line, count=1)

# выводим полученную строку (с заменой или без, если IP не найден)
print(modified_line)
