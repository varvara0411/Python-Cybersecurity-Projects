import hmac
import hashlib

# --- Функция создания подписи ---
def sign_message(message, secret_key):
    """
    Создает HMAC-SHA256 подпись для сообщения.

    Args:
        message (str): Сообщение для подписи.
        secret_key (str): Секретный ключ.

    Returns:
        str: Подпись в виде шестнадцатеричной строки.
    """
    # преобразуем message и secret_key в байты
    message_bytes = message.encode('utf-8')
    key_bytes = secret_key.encode('utf-8')

    # создаем объект HMAC с использованием SHA-256
    h = hmac.new(key_bytes, message_bytes, hashlib.sha256)

    # Получаем подпись в виде hex-строки
    signature_hex = h.hexdigest()

    return signature_hex

# --- Функция проверки подписи ---
def verify_signature(message, signature, secret_key):
    """
    Проверяет HMAC-SHA256 подпись для сообщения.

    Args:
        message (str): Сообщение.
        signature (str): Подпись в виде шестнадцатеричной строки для проверки.
        secret_key (str): Секретный ключ.

    Returns:
        bool: True, если подпись верна, иначе False.
    """
    # преобразуем message и secret_key в байты
    message_bytes = message.encode('utf-8')
    key_bytes = secret_key.encode('utf-8')

    # пересчитываем ожидаемую подпись
    h_expected = hmac.new(key_bytes, message_bytes, hashlib.sha256)
    expected_signature_hex = h_expected.hexdigest()

    # безопасное сравнение подписей
    return hmac.compare_digest(expected_signature_hex, signature)

if __name__ == '__main__':
    
    # ввод данных от пользователя
    message = input("Сообщение: ")
    secret_key = input("Секретный ключ: ")
   
    # создаем подпись
    signature = sign_message(message, secret_key)
    print(f"Созданная подпись: {signature}")
    
    # проверка: корректная ли подпись
    is_valid = verify_signature(message, signature, secret_key)
    print(f"Результат проверки корректности подписи: {is_valid}")
