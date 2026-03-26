import hashlib
import itertools

def brute_force_attack(password_hash, charset, max_length):
    """
    Перебирает пароли, чтобы найти соответствие хешу.

    Args:
        password_hash (str): MD5 хеш пароля.
        charset (str): Набор символов для перебора.
        max_length (int): Максимальная длина перебираемых паролей.

    Returns:
        str: Найденный пароль или "PASSWORD NOT FOUND".
    """
    # проходим по всем длинам паролей от 1 до max_length (включительно)
    for length in range(1, max_length + 1):
        # генерируем все возможные комбинации символов заданной длины
        for combination in itertools.product(charset, repeat=length):
            # преобразуем комбинацию в строку
            password_candidate = ''.join(combination)
            # вычисляем хеш для текущего кандидата
            hash_candidate = hashlib.md5(password_candidate.encode()).hexdigest()
            # сравниваем с целевым хешем
            if hash_candidate == password_hash:
                return password_candidate
    return "PASSWORD NOT FOUND"


if __name__ == "__main__":
    # вводим пароль из 5 букв английского алфавита (a-z), который будем искать
    test_password = input("Пароль из 5 букв английского алфавита (a-z): ")
    
    # вычисляем его MD5-хеш
    test_hash = hashlib.md5(test_password.encode()).hexdigest()
    
    # запускаем атаку
    result = brute_force_attack(
        password_hash=test_hash,
        charset="abcdefghijklmnopqrstuvwxyz",
        max_length=5
    )
    
    print(f"Результат: {result}")
    
    if result == test_password:
        print("Успех! Пароль найден!")
    else:
        print("Ошибка! Пароль не найден!")
