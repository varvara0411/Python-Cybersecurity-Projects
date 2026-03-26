import sys
import re
import json
from collections import defaultdict, Counter

def parse_auth_log(log_lines):
    """
    Анализирует строки лога аутентификации и возвращает статистику
    по успешным и неудачным попыткам входа.
    """
    # регулярные выражения для извлечения информации
    # ищем строки с успешной аутентификацией (Accepted) и извлекаем имя пользователя и IP
    successful_pattern = r"sshd\[\d+\]: Accepted (?:password|publickey) for (?:invalid user )?(\S+) from (\S+)"
    # ищем строки с неудачной аутентификацией (Failed) и извлекаем имя пользователя и IP
    failed_pattern = r"sshd\[\d+\]: Failed (?:password|publickey) for (?:invalid user )?(\S+) from (\S+)"
    
    # счетчики и структуры данных для сбора статистики
    successful_count = 0  # общее количество успешных попыток
    failed_count = 0      # общее количество неудачных попыток
    successful_users = Counter()  # счетчик успешных попыток по пользователям
    failed_users = Counter()      # счетчик неудачных попыток по пользователям
    successful_ips = Counter()    # счетчик успешных попыток по IP-адресам
    failed_ips = Counter()        # счетчик неудачных попыток по IP-адресам
    
    # снализ каждой строки лога
    for line in log_lines:
        line = line.strip()
        if not line:
            continue
        
        # проверка на успешную авторизацию
        successful_match = re.search(successful_pattern, line)
        if successful_match:
            user, ip = successful_match.groups()
            ip = ip.split()[0]  # извлекаем только IP-адрес, убирая порт и другие данные
            
            successful_count += 1
            successful_users[user] += 1
            successful_ips[ip] += 1
            continue
        
        # проверка на неудачную авторизацию
        failed_match = re.search(failed_pattern, line)
        if failed_match:
            user, ip = failed_match.groups()
            ip = ip.split()[0]  # извлекаем только IP-адрес
            
            failed_count += 1
            failed_users[user] += 1
            failed_ips[ip] += 1
    
    # формируем результат
    result = {
        "summary": {
            "successful_attempts": successful_count,
            "failed_attempts": failed_count,
            "total_attempts": successful_count + failed_count
        },
        "users": {
            "successful": {user: count for user, count in successful_users.most_common()},
            "failed": {user: count for user, count in failed_users.most_common()}
        },
        "ips": {
            "successful": {ip: count for ip, count in successful_ips.most_common()},
            "failed": {ip: count for ip, count in failed_ips.most_common()}
        }
    }
    
    return result

if __name__ == "__main__":
    # считываем данные из стандартного ввода
    log_data = sys.stdin.read().strip()
    log_lines = log_data.splitlines()
    
    # анализируем лог и получаем статистику
    auth_stats = parse_auth_log(log_lines)
    
    # выводим результат в формате JSON с отступами для читаемости
    print(json.dumps(auth_stats, indent=2))
