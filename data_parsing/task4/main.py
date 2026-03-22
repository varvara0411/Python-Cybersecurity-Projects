
import xml.etree.ElementTree as ET
import sys

# считываем всю XML-строку из стандартного ввода
xml_input = sys.stdin.read()

host_count = 0 # значение по умолчанию
try:
    # парсим XML-строку
    root = ET.fromstring(xml_input)

    # ищем ВСЕ непосредственные дочерние элементы с тегом 'host'
    # findall() возвращает список найденных элементов (или пустой список)
    host_elements = root.findall('host')

    # подсчитываем количество элементов в полученном списке
    host_count = len(host_elements)

except ET.ParseError:
    # если входные данные - невалидный XML, считаем, что найдено 0 хостов
    print("Error: Invalid XML input") 
    host_count = 0

# выводим итоговое количество хостов (целое число)
print(host_count)
