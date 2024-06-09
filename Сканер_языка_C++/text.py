# Драйвер исходного текста
from glob import glob
import sys
import loc
import error

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
                    src += chEOT
                    print(file_name)
                    file.close()
        else:
            error.Error('Ошибка открытия файла, такого файла не существует')


def next_ch():
    global src, i, ch, line
    ch = src[i]
    loc.pos += 1
    i += 1
    if ch in '\n\r':
        ch = chEOL
        loc.pos = 0
    elif ch == chEOT:
        ch = chEOT
        loc.pos = 0
        return
    print(ch, end='')
