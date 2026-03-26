import sys
import re
import json
from collections import Counter

# действия, считающиеся блокировкой (можно расширить)
BLOCKED_ACTIONS = {"BLOCK", "DROP", "DENY", "REJECT"}
# количество элементов для вывода в топах
TOP_N = 5

def parse_firewall_log(log_lines):
    """
    Анализирует строки лога файрвола, выявляет заблокированные соединения
    и возвращает статистику по ним.
    """
    # регулярное выражение для извлечения ключевых полей из логов UFW-подобного формата
    # группа 1: Действие (BLOCK, ALLOW, etc.)
    # группа 2: IP-адрес источника (SRC)
    # группа 3: Порт назначения (DPT)
    log_pattern = re.compile(r"\[UFW (ALLOW|BLOCK|DENY|REJECT|DROP)\] .* SRC=(\S+) .* DPT=(\d+)")
    
    total_blocked = 0           # общий счетчик заблокированных пакетов
    blocked_src_ips = Counter() # счетчик заблокированных IP источников
    blocked_dst_ports = Counter() # счетчик заблокированных портов назначения
    
    # обрабатываем каждую строку лога
    for line in log_lines:
        line = line.strip()
        if not line: # пропускаем пустые строки
            continue
            
        # ищем совпадение с нашим шаблоном
        match = log_pattern.search(line)
        if match:
            # извлекаем захваченные группы
            action, src_ip, dst_port_str = match.groups()
            
            # проверяем, является ли действие блокирующим
            if action in BLOCKED_ACTIONS:
                total_blocked += 1
                blocked_src_ips[src_ip] += 1
                try:
                    # преобразуем порт в число и увеличиваем счетчик
                    dst_port = int(dst_port_str)
                    blocked_dst_ports[dst_port] += 1
                except ValueError:
                    # игнорируем, если порт не является числом (маловероятно с этим regex, но на всякий случай)
                    pass
                    
    # формируем итоговый отчет в виде словаря
    report = {
        "total_blocked_packets": total_blocked,
        # берем TOP_N самых частых IP и преобразуем в словарь
        f"top_{TOP_N}_blocked_source_ips": dict(blocked_src_ips.most_common(TOP_N)),
        # берем TOP_N самых частых портов и преобразуем в словарь
        f"top_{TOP_N}_blocked_destination_ports": dict(blocked_dst_ports.most_common(TOP_N))
    }
    
    return report

if __name__ == "__main__":
    # считываем данные из стандартного ввода
    log_data = sys.stdin.read().strip()
    log_lines = log_data.splitlines()
    
    # анализируем лог и получаем статистику
    firewall_report = parse_firewall_log(log_lines)
    
    # выводим результат в формате JSON с отступами
    print(json.dumps(firewall_report, indent=2))

