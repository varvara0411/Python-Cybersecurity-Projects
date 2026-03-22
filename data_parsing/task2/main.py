import xml.etree.ElementTree as ET
import sys

# считываем всю XML-строку из стандартного ввода
xml_input = sys.stdin.read()

try:
    # парсим XML-строку в древовидную структуру элементов
    # root - это корневой элемент XML
    root = ET.fromstring(xml_input)

    # ищем первый дочерний элемент с тегом 'service' внутри корневого элемента
    service_element = root.find('service')

    # проверяем, был ли найден элемент 
    if service_element is not None:
        # если найден, пытаемся получить значение атрибута 'name'
        # метод .get() вернет None, если атрибут отсутствует
        service_name = service_element.get('name')

        # проверяем, был ли атрибут 'name' найден (значение не None)
        if service_name is not None:
            # выводим значение атрибута
            print(service_name)
        # если атрибут 'name' отсутствует у тега , ничего не выводим

    # если тег  не найден (service_element is None), ничего не выводим

except ET.ParseError:
    # обработка на случай, если входная строка - невалидный XML
    print("Error: Invalid XML input") 

