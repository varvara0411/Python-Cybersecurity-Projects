import subprocess
import sys
from datetime import datetime

def get_process_count():
    """
    Получает количество процессов через команду ps axl --no-headers
    """
    try:
        # запускаем ps axl с опцией --no-headers (без заголовка)
        result = subprocess.run(
            ['ps', 'axl', '--no-headers'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # считаем непустые строки (все строки - это процессы, без заголовка)
        lines = [line for line in result.stdout.strip().split('\n') if line.strip()]
        return len(lines)
        
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return None

def main():
    # параметры нормального диапазона
    min_normal = 50
    max_normal = 500
    
    # получаем количество процессов
    count = get_process_count()
    
    if count is None:
        print("Не удалось получить количество процессов")
        sys.exit(1)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Текущее количество процессов: {count}")
    print(f"Нормальный диапазон: {min_normal} – {max_normal}")
    print(f"Время проверки: {timestamp}")
    
    # проверяем на аномалию
    if count < min_normal:
        print(f"АНОМАЛИЯ: {count} процессов НИЖЕ нормы!")
        print(f"Не хватает {min_normal - count} процессов до нормы")
        sys.exit(1)
    elif count > max_normal:
        print(f"АНОМАЛИЯ: {count} процессов ВЫШЕ нормы!")
        print(f"Превышение на {count - max_normal} процессов")
        sys.exit(1)
    else:
        print(f"Количество процессов в норме")
        sys.exit(0)

if __name__ == "__main__":
    main()