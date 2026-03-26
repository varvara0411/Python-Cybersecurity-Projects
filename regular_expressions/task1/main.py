
import re

# считываем строку лога из стандартного ввода
log_line = input()

# задаем шаблон для поиска - слово "ERROR"
pattern_to_find = "ERROR"

# выполняем поиск шаблона в строке лога
# re.IGNORECASE (или re.I) делает поиск нечувствительным к регистру
match_result = re.search(pattern_to_find, log_line, re.IGNORECASE)

# проверяем результат поиска.
# если re.search() нашел совпадение, он вернет объект Match (который в bool() дает True).
# если совпадений нет, он вернет None (который в bool() дает False).
found = bool(match_result)

# выводим результат (True или False)
print(found)
