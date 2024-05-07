# Данный модуль содержит чтение и обработку текста (unicode и escape тоже)
from glob import glob
import sys
import Positions
import Errors
from string import hexdigits

chEOT = '\0'
chEOL = '\n'
chSPACE = ' '
chHT = '\t'
chFF = '\f'
src = ""
i = 0
ch = ""
file_list = []
line = ''
slash = False


def reset():
    global src, file_list
    if len(sys.argv) < 2:
        Errors.Error("Запуск: python C++.py <файл программы>")
    else:
        file_list = glob(sys.argv[1])
        if file_list:
            for file_name in file_list:
                with open(file_name, 'r', encoding='utf-8') as file:
                    src += file.read()
                    print(file_name)
                    file.close()
        else:
            Errors.Error('Такого файла не существует')


def string_to_integer_by_16(string):
    hex_digits = '0123456789ABCDEF'
    result = 0
    for char in string:
        digit = hex_digits.index(char.upper())
        result = result * 16 + digit
    return result


def unicode_escape():
    global ch, slash
    slash = False
    next_ch()
    unicode = ''
    while ch == 'u':
        next_ch()
    if ch == '\\':
        next_ch()
    if ch == 'u':
        next_ch()
    for _ in range(3):
        if ch in hexdigits:
            unicode += ch
            next_ch()
        else:
            Errors.lexError('Unicode дописан не до конца')
    if ch in hexdigits:
        unicode += ch
    else:
        Errors.lexError('Unicode дописан не до конца')
    # print('Unicode =', unicode)
    return chr(string_to_integer_by_16(unicode))


def next_ch():
    global src, i, ch, line, slash
    if i < len(src):
        ch = src[i]
        line += ch
        Positions.pos += 1
        i += 1
        if not slash:
            print(ch, end='')
        if ch == '\\':
            slash = True
            next_ch()
            if ch == 'u':
                print('u', end='')
                ch = unicode_escape()
            else:
                ch = '\\'
                Positions.pos -= 1
                i -= 1
                slash = False
        if ch in '\n\r':
            # print(line, end='')
            line = ''
            ch = chEOL
            Positions.pos = 0
    else:
        ch = chEOT