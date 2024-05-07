from string import digits

# Открываем файл для чтения и считываем его содержимое
with open('output.txt', 'r', encoding='utf-8') as file:
    cpp_letter = file.read()
cpp_letter_or_digit = cpp_letter + digits

integer_type_suffix = 'uUlL'
float_type_suffix = 'fFlL'
exponent_indicator = 'eEpP'
sign = '+-'
