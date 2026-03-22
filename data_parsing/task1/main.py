import sys

target_key = "LISTEN_PORT"

# Сначала читаем все строки из ввода
lines = sys.stdin.readlines()

# А потом ищем нужную строку
for line in lines:
    if line.startswith(target_key):
        parts = line.split('=', 1)
        if len(parts) == 2:
            print(parts[1].strip())
            break 