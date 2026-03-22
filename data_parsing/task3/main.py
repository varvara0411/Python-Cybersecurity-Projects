import xml.etree.ElementTree as ET
import sys

# считываем всю XML-строку из стандартного ввода
xml_input = sys.stdin.read()

try:
    # парсим XML-строку
    root = ET.fromstring(xml_input)

    # ищем первый дочерний элемент с тегом 'message'
    message_element = root.find('message')

    # проверяем, был ли найден элемент 
    if message_element is not None:
        # если найден, получаем его текстовое содержимое
        # атрибут .text будет None, если текста нет
        message_text = message_element.text

        # проверяем, есть ли текст (не None)
        if message_text is not None:
            # выводим текст
            print(message_text) # Выводим как есть

except ET.ParseError:
    # обработка на случай, если входная строка - невалидный XML
    print("Error: Invalid XML input") 