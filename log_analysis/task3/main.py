import sys
import re
from urllib.parse import unquote

# Алгоритм решения:
# 1. Определить регулярные выражения для поиска потенциальных SQL-инъекций и XSS-атак
# 2. Определить регулярное выражение для парсинга строки лога веб-сервера (извлечение запроса)
# 3. Считать данные из стандартного ввода
# 4. Инициализировать список для хранения подозрительных логов
# 5. Для каждой строки лога:
#    a. Распарсить строку, извлечь часть с запросом (URL + параметры)
#    b. Декодировать URL-кодированные символы в запросе (например, %27 -> ')
#    c. Проверить декодированный запрос на наличие паттернов SQL-инъекций
#    d. Проверить декодированный запрос на наличие паттернов XSS-атак
#    e. Если найден хотя бы один паттерн, добавить исходную строку лога в список подозрительных
# 6. Вывести список подозрительных строк лога, каждая на новой строке

# паттерны для обнаружения атак (упрощенные)
# используем re.compile для компиляции регулярных выражений для повышения производительности
# re.IGNORECASE делает поиск регистронезависимым
SQLI_PATTERNS = [
    re.compile(r"(\'|\%27)|(\-\-)|(\bUNION\b.*\bSELECT\b)|(\bOR\b.*\b\=\b)", re.IGNORECASE),
    re.compile(r"/\*.*?\*/", re.IGNORECASE),
    re.compile(r"\bsleep\(\s*\d+\s*\)", re.IGNORECASE)
]
XSS_PATTERNS = [
    re.compile(r"(<script>)|(%3Cscript%3E)|(alert\()|(onerror=)|(onload=)|(<iframe)|(%3Ciframe)", re.IGNORECASE),
    re.compile(r"\bdocument\.cookie\b", re.IGNORECASE)
]

def parse_log_line(line):
    """
    Парсит строку лога веб-сервера (Common Log Format) и извлекает из нее часть с запросом.
    Формат лога: IP - - [timestamp] "METHOD /path HTTP/version" status size
    Возвращает строку вида "METHOD /path HTTP/version" или None.
    """
    # регулярное выражение для парсинга Common Log Format
    # захватывает весь блок запроса ("METHOD /path HTTP/version") во вторую группу
    pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} - - \[(.*?)\] "(.*?)" \d{3} (?:\d+|-)'
    match = re.match(pattern, line)
    if match:
        return match.group(2)  # возвращаем вторую группу (запрос)
    return None

def check_for_attacks(request_string, sqli_patterns, xss_patterns):
    """
    Проверяет строку запроса на наличие паттернов SQL-инъекций и XSS-атак.
    Возвращает True, если найден хотя бы один паттерн, иначе False.
    """
    # декодируем URL-кодированные символы (%27 -> ', %3C -> <, и т.д.)
    # используем unquote несколько раз на случай двойного кодирования
    try:
        decoded_request = unquote(unquote(request_string))
    except Exception:
        # в случае ошибки декодирования, работаем с исходной строкой
        decoded_request = request_string

    # проверяем на наличие паттернов SQL-инъекций
    for pattern in sqli_patterns:
        if pattern.search(decoded_request):
            return True  # найдена потенциальная SQL-инъекция

    # проверяем на наличие паттернов XSS-атак
    for pattern in xss_patterns:
        if pattern.search(decoded_request):
            return True  # найден потенциальный XSS

    # если ни один паттерн не сработал
    return False

if __name__ == "__main__":
    # считываем данные из стандартного ввода
    # strip() удаляет начальные и конечные пробелы и символы новой строки
    log_data = sys.stdin.read().strip()
    # splitlines() разделяет входные данные на список строк
    log_lines = log_data.splitlines()

    suspicious_logs = []

    # обрабатываем каждую строку лога
    for line in log_lines:
        # strip() для каждой строки на случай лишних пробелов
        line = line.strip()
        if not line:  # пропускаем пустые строки
            continue

        # парсим строку лога, чтобы извлечь часть с запросом
        request_part = parse_log_line(line)

        # если удалось успешно извлечь часть запроса
        if request_part:
            # проверяем извлеченный запрос на наличие паттернов атак
            if check_for_attacks(request_part, SQLI_PATTERNS, XSS_PATTERNS):
                # если найден подозрительный паттерн, добавляем исходную строку лога в список
                suspicious_logs.append(line)

    # выводим отсортированный результат (каждый подозрительный лог на новой строке)
    # sorted() сортирует список в алфавитном порядке
    for log in sorted(suspicious_logs):
        print(log)