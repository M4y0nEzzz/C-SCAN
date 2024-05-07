#Модуль создает основу для анализа кода на плюсах.
#Определяются переменные, используемые для
#идентификации различных типов числовых литералов.

from string import digits

# Открываем и читаем файл
with open('output.txt', 'r', encoding='utf-8') as file:
    cpp_letter = file.read()
cpp_letter_or_digit = cpp_letter + digits

integer_type_suffix = 'uUlL'
float_type_suffix = 'fFlL'
exponent_indicator = 'eEpP'
sign = '+-'
