# Данный модуль содержит сообщения об ошибках
import Positions
import Text


def _error(msg, p):
    while Text.ch not in {Text.chEOL, Text.chEOT}:
        Text.next_ch()
    print(' ' * (p - 1), '^', sep='')
    print(msg)
    exit(1)


def lexError(msg):
    _error('Лексическая ошибка: ' + msg, Positions.pos)


def expect(msg):
    _error("Ожидается " + msg, Positions.lexPos)


def ctxError(msg):
    _error(msg, Positions.lexPos)


def Error(msg):
    print()
    print(msg)
    exit(2)


def Warning(msg):
    print()
    print(msg)