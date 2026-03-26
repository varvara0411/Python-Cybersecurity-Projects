import sys
import re
import json
from collections import Counter

# порог для определения потенциального брутфорса
# (количество неудачных попыток с одного IP)
BRUTE_FORCE_THRESHOLD = 5

def find_suspicious_ips(log_lines, threshold):
    """
    Анализирует строки лога аутентификации и возвращает список IP-адресов,
    с которых было совершено больше неудачных попыток входа, чем указано в threshold.
    """
    # регулярное выражение для поиска неудачных попыток SSH и извлечения IP-адреса
    # ищет строки с "sshd", "Failed password" или "Failed publickey"
    # захватывает IP-адрес (и порт) в первую группу
    failed_pattern = r"sshd\[\d+\]: Failed (?:password|publickey) for (?:invalid user )?\S+ from (\S+)"
    
    # используем Counter для подсчета неудачных попыток по каждому IP
    failed_ips_counter = Counter()
    
    # анализ каждой строки лога
    for line in log_lines:
        line = line.strip()
        if not line:  # пропускаем пустые строки
            continue
        
        # ищем совпадение с шаблоном неудачной попытки
        failed_match = re.search(failed_pattern, line)
        if failed_match:
            # извлекаем первую группу (IP-адрес с портом)
            ip_with_details = failed_match.group(1)
            # очищаем IP-адрес, беря только первую часть до пробела
            ip = ip_with_details.split()[0]
            # увеличиваем счетчик для данного IP
            failed_ips_counter[ip] += 1
            
    # фильтрация IP-адресов: выбираем те, у которых счетчик > threshold
    suspicious_ips = [ip for ip, count in failed_ips_counter.items() if count > threshold]
    
    return suspicious_ips

if __name__ == "__main__":
    # считываем данные из стандартного ввода
    log_data = sys.stdin.read().strip()
    log_lines = log_data.splitlines()
    
    # ищем подозрительные IP-адреса, используя заданный порог
    suspicious_ips = find_suspicious_ips(log_lines, BRUTE_FORCE_THRESHOLD)
    
    # выводим отсортированный результат (каждый IP на новой строке)
    for ip in sorted(suspicious_ips):
        print(ip)
