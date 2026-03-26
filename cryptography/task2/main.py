import hashlib
import sys  # импортируем sys для чтения из stdin

def hash_password(password, salt):
    """
    Вычисляет хеш SHA-256 для строки (пароль + соль).

    :param password: Строка с паролем.
    :param salt: Строка с солью.
    :return: Строка с шестнадцатеричным представлением хеша SHA-256.
    """

    # объединяем пароль и соль (password + salt) в одну строку
    combined_string = password + salt 
    
    # преобразуем объединенную строку в байты с помощью encode('utf-8')
    combined_bytes = combined_string.encode('utf-8') 
    
    # создаем объект хеширования SHA-256 и передаем байты объекту хеширования
    hash_object = hashlib.sha256(combined_bytes)  
       
    # получаем хеш в виде шестнадцатеричной строки (метод hexdigest())
    hex_digest = hash_object.hexdigest()  
    
    # возвращаем полученный хеш
    return hex_digest

# читаем данные и вызываем функцию hash_password,
# а затем выводим результат
if __name__ == '__main__':
    # читаем одну строку из стандартного ввода
    line = sys.stdin.readline().strip() 
    
    # Разделяем строку по первому символу ':'
    try:
        input_password, input_salt = line.split(':', 1)
    except ValueError:
        print("Ошибка: Неверный формат входных данных. Ожидается 'пароль:соль'.")
        sys.exit(1)  # выходим с ошибкой

    # вызываем функцию для вычисления хеша
    calculated_hash = hash_password(input_password, input_salt)
    
    # выводим результат в стандартный вывод
    print(calculated_hash)