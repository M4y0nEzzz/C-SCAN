# Драйвер исходного текста
from glob import glob
import sys
import loc
import error
from sets import hexadecimal_digit

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
        error.Error("Запуск: python CPP.py <файл программы>")
    else:
        file_list = glob(sys.argv[1])
        if file_list:
            for file_name in file_list:
                with open(file_name, 'r', encoding='utf-8') as file:
                    src += file.read()
                    print(file_name)
                    file.close()
        else:
            error.Error('Ошибка открытия файла, такого файла не существует')


def string_to_integer_by_16(string):
    result = 0
    for char in string:
        digit = hexadecimal_digit.index(char.upper())
        result = result * 16 + digit
    return result


def unicode_escape():
    global ch, slash
    slash = False
    next_ch()
    if ch == 'u':
        universal_character_name = ''
        while ch == 'u':
            next_ch()
        for _ in range(3):
            if ch in hexadecimal_digit:
                universal_character_name += ch
                next_ch()
            else:
                error.lexError('UCN дописан не до конца')
        if ch in hexadecimal_digit:
            universal_character_name += ch
        else:
            error.lexError('UCN дописан не до конца')
        # print('Unicode =', unicode)
        return chr(string_to_integer_by_16(universal_character_name))
    elif ch == 'U':
        universal_character_name = ''
        while ch == 'U':
            next_ch()
        for _ in range(7):
            if ch in hexadecimal_digit:
                universal_character_name += ch
                next_ch()
            else:
                error.lexError('UCN дописан не до конца')
        if ch in hexadecimal_digit:
            universal_character_name += ch
        else:
            error.lexError('UCN дописан не до конца')
        # print('Unicode =', unicode)
        return chr(string_to_integer_by_16(universal_character_name))


def next_ch():
    global src, i, ch, line, slash
    if i < len(src):
        ch = src[i]
        line += ch
        loc.pos += 1
        i += 1
        if not slash:
            print(ch, end='')
        if ch == '\\':
            slash = True
            next_ch()
            if ch == 'u':
                print('u', end='')
                ch = unicode_escape()
            if ch == 'U':
                print('U', end='')
                ch = unicode_escape()
            else:
                ch = '\\'
                loc.pos -= 1
                i -= 1
                slash = False
        if ch in '\n\r':
            # print(line, end='')
            line = ''
            ch = chEOL
            loc.pos = 0
    else:
        ch = chEOT