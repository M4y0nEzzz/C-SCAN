# Лексический анализатор C++
from enum import Enum
from string import octdigits, hexdigits

import error
from text import next_ch
import text
from sets import *



class Lex(Enum):
    (AND, ANDEQ, ASM, AUTO, BITAND, BITOR, BOOL, BREAK, CASE,
    CONTINUE, DEFAULT, DELETE, DO, DOUBLE, DYNAMIC_CAST, ELSE, ENUM, EXPLICIT,
    GOTO, IF, INLINE, INT, LONG, MUTABLE, NAMESPACE, NEW, NOT,
    PUBLIC, REGISTER, REINTERPRETCAST, RETURN, SHORT, SIGNED, SIZEOF, STATIC, STATICCAST,
    TRY, TYPEDEF, TYPEID, TYPENAME, UNION, UNSIGNED, USING, VIRTUAL, VOID,
    CATCH, CHAR, CLASS, COMPL, CONST, CONSTAST, EXPORT, EXTERN, FALSE, FLOAT, FOR, FRIEND,
    NOTEQ, OPERATOR, OR, OREQ, PRIVATE, PROTECTED, STRUCT, SWITCH, TEMPLATE, THIS, THROW, TRUE,
    VOLATILE, WCHART, WHILE, XOR, XOREQ, STRING,
    SELECT, VAR, INCLUDE,
    PLUS, MINUS, MUL, DIV, MOD,
    CARET, LTLT, GTGT, ANDCARET,
    PLUSEQ, MINUSEQ, MULEQ, DIVEQ, MODEQ, COUT, MAP, MINUSARROW,
    CARETEQ, LTLTEQ, GTGTEQ, ANDCARETEQ,
    ANDAND, OROR, LTMINUS, INC, DEC,
    EQEQ, LT, GT, EQ, TILDA,
    NE, LE, GE, ASS, THREEDOT,
    LPAR, RPAR, LSQPAR, RSQPAR, BEGIN, END,
    COMMA, DOT, SEMI, COLON, IDENTIFIER, EOT,
    INTEGERLIT, COMPLEXLIT, RUNELIT, STRINGLIT, FLOATLIT) = range(131)


lex_names = []
for enum_lex in Lex:
    lex_names.append(enum_lex.name)
lex_dict = dict(zip(lex_names, [0] * len(Lex)))
name = ''

keywords = {
    'and': Lex.AND,
    'and_ed': Lex.ANDEQ,
    'asm': Lex.ASM,
    'auto': Lex.AUTO,
    'bitand': Lex.BITAND,
    'bitor': Lex.BITOR,
    'bool': Lex.BOOL,
    'break': Lex.BREAK,
    'case': Lex.CASE,
    'continue': Lex.CONTINUE,
    'cout': Lex.COUT,
    'default': Lex.DEFAULT,
    'delete': Lex.DELETE,
    'do': Lex.DO,
    'double': Lex.DOUBLE,
    'dynamic_cast': Lex.DYNAMIC_CAST,
    'else': Lex.ELSE,
    'enum': Lex.ENUM,
    'explicit': Lex.EXPLICIT,
    'goto': Lex.GOTO,
    'if': Lex.IF,
    'inline': Lex.INLINE,
    'int': Lex.INT,
    'long': Lex.LONG,
    'mutable': Lex.MUTABLE,
    'map': Lex.MAP,
    'namespace': Lex.NAMESPACE,
    'new': Lex.NEW,
    'not': Lex.NOT,
    'public': Lex.PUBLIC,
    'register': Lex.REGISTER,
    'reinterpret_cast': Lex.REINTERPRETCAST,
    'return': Lex.RETURN,
    'short': Lex.SHORT,
    'signed': Lex.SIGNED,
    'sizeof': Lex.SIZEOF,
    'static': Lex.STATIC,
    'static_cast': Lex.STATICCAST,
    'try': Lex.TRY,
    'typedef': Lex.TYPEDEF,
    'typename': Lex.TYPENAME,
    'union': Lex.UNION,
    'unsigned': Lex.UNSIGNED,
    'using': Lex.USING,
    'virtual': Lex.VIRTUAL,
    'void': Lex.VOID,
    'catch': Lex.CATCH,
    'char': Lex.CHAR,
    'class': Lex.CLASS,
    'compl': Lex.COMPL,
    'const': Lex.CONST,
    'const_cast': Lex.CONSTAST,
    'export': Lex.EXPORT,
    'extern': Lex.EXTERN,
    'false': Lex.FALSE,
    'float': Lex.FLOAT,
    'for': Lex.FOR,
    'friend': Lex.FRIEND,
    'not_eq': Lex.NOTEQ,
    'operator': Lex.OPERATOR,
    'or': Lex.OR,
    'or_eq ': Lex.OREQ,
    'private': Lex.PRIVATE,
    'protected': Lex.PROTECTED,
    'struct': Lex.STRUCT,
    'switch': Lex.SWITCH,
    'template': Lex.TEMPLATE,
    'this': Lex.THIS,
    'throw': Lex.THROW,
    'true': Lex.TRUE,
    'volatile': Lex.VOLATILE,
    'wchar_t': Lex.WCHART,
    'while': Lex.WHILE,
    'xor': Lex.XOR,
    'xor_eq': Lex.XOREQ,
    '#include': Lex.INCLUDE,
    'string': Lex.STRING
}

def traditional_comment():
    next_ch()
    while True:
        if text.ch == '/':
            next_ch()
            if text.ch == '/':
                next_ch()
                break
        elif text.ch == text.chEOT:
            error.lexError('Не закончен комментарий')
        else:
            next_ch()


def place_imp():
    next_ch()
    while True:
        if text.ch == '#':
            next_ch()
            break
        elif text.ch == text.chEOT:
            error.lexError('Не закончен местный импорт')
        else:
            next_ch()

def end_of_the_line_comment():
    next_ch()
    while text.ch not in {text.chEOL, text.chEOT}:
        next_ch()


def binary_lit():
    next_ch()
    if text.ch in '_':
        next_ch()
    if text.ch in '01':
        # binary_digits
        next_ch()
        while True:
            if text.ch in '_':
                next_ch()
                if text.ch in '01':
                    next_ch()
                    continue
                else:
                    error.lexError('Ожидается 0 или 1')
            elif text.ch in '01':
                next_ch()
                continue
            else:
                break


def octal_lit():
    next_ch()
    if text.ch in '_':
        next_ch()
    if text.ch in octdigits:
        # binary_digits
        next_ch()
        while True:
            if text.ch in '_':
                next_ch()
                if text.ch in octdigits:
                    next_ch()
                    continue
                else:
                    error.lexError('Ожидается octdigits')
            elif text.ch in octdigits:
                next_ch()
                continue
            else:
                break


def decimal_digits():
    if text.ch in digits:
        next_ch()
        while True:
            if text.ch in '_':
                next_ch()
                if text.ch in digits:
                    next_ch()
                    continue
                else:
                    error.lexError('Ожидается десятичные цифры')
            elif text.ch in digits:
                next_ch()
                continue
            else:
                break
    else:
        error.lexError('Ожидается десятичная цифра')


def hex_digits():
    if text.ch in hexdigits:
        next_ch()
        while True:
            if text.ch in '_':
                next_ch()
                if text.ch in hexdigits:
                    next_ch()
                    continue
                else:
                    error.lexError('Ожидается шестнадцатеричная цифра')
            elif text.ch in hexdigits:
                next_ch()
                continue
            else:
                break
    else:
        error.lexError('Ожидается шестнадцатеричная цифра')


def decimal_exponent():
    next_ch()  # пропустили eE
    if text.ch in '+-':
        next_ch()
    decimal_digits()


def hex_exponent():
    if text.ch in 'pP':
        next_ch()
        if text.ch in '+-':
            next_ch()
        decimal_digits()
    else:
        error.lexError('Ожидается p или P')


def little_u_value():
    next_ch()  # пропустили 'u'
    for _ in range(4):
        if text.ch in hexdigits:
            next_ch()
        else:
            error.lexError('unicode дописан не до конца')


def big_u_value():
    next_ch()  # пропустили 'U'
    for _ in range(8):
        if text.ch in hexdigits:
            next_ch()
        else:
            error.lexError('Unicode дописан не до конца')


def octal_byte_value():
    for _ in range(3):
        if text.ch in octdigits:
            next_ch()
        else:
            error.lexError('OctalByteValue дописан не до конца')


def hex_byte_value():
    next_ch()  # пропустили 'x'
    for _ in range(2):
        if text.ch in hexdigits:
            next_ch()
        else:
            error.lexError('HexByteValue дописан не до конца')


def next_lex():
    global name, lex
    while text.ch in {text.chSPACE, text.chHT, text.chFF}:
        next_ch()
    match text.ch:
        case text.chEOL:
            next_ch()
            if lex in {Lex.INTEGERLIT, Lex.FLOATLIT, Lex.COMPLEXLIT, Lex.STRINGLIT,
                       Lex.BREAK, Lex.CONTINUE, Lex.RETURN,
                       Lex.INC, Lex.DEC}:
                lex = Lex.SEMI
            else:
                next_lex()

        # Идентификаторы и служебные слова
        case _ if text.ch in letter:
            name = text.ch
            next_ch()
            while text.ch in letter or text.ch in digits:  # !!!!!
                name += text.ch
                next_ch()
            lex = keywords.get(name, Lex.IDENTIFIER)

        # Разделители
        case '(':
            next_ch()
            lex = Lex.LPAR
        case ')':
            next_ch()
            lex = Lex.RPAR
        case '{':
            next_ch()
            lex = Lex.BEGIN
        case '}':
            next_ch()
            lex = Lex.END
        case '[':
            next_ch()
            lex = Lex.LSQPAR
        case ']':
            next_ch()
            lex = Lex.RSQPAR
        case ';':
            next_ch()
            lex = Lex.SEMI
        case ',':
            next_ch()
            lex = Lex.COMMA
        case '.':  # !!!!!!
            next_ch()
            if text.ch == '.':
                next_ch()
                if text.ch == '.':
                    next_ch()
                    lex = Lex.THREEDOT
                else:
                    error.lexError('Должно быть три точки')
            elif text.ch in digits:
                decimal_digits()
                if text.ch in 'eE':
                    decimal_exponent()
                lex = Lex.FLOATLIT
            else:
                lex = Lex.DOT

        # Операции
        case '=':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.EQEQ
            else:
                lex = Lex.EQ
        case '+':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.PLUSEQ
            elif text.ch == '+':
                next_ch()
                lex = Lex.INC
            else:
                lex = Lex.PLUS
        case '>':
            next_ch()
            if text.ch == '=':  # >=
                next_ch()
                lex = Lex.GE
            elif text.ch == '>':  # >>
                next_ch()
                if text.ch == '=':  # >>=
                    next_ch()
                    lex = Lex.GTGTEQ
                else:  # >>
                    lex = Lex.GTGT
            else:  # >
                lex = Lex.GT
        case '<':
            next_ch()
            if text.ch == '=':  # <=
                next_ch()
                lex = Lex.LE
            elif text.ch == '<':  # <<
                next_ch()
                if text.ch == '=':  # <<=
                    next_ch()
                    lex = Lex.LTLTEQ
                else:  # <<
                    lex = Lex.LTLT
            else:  # <
                lex = Lex.LT
        case '-':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.MINUSEQ
            elif text.ch == '-':
                next_ch()
                lex = Lex.DEC
            elif text.ch == '>':
                next_ch()
                lex = Lex.MINUSARROW
            else:
                lex = Lex.MINUS
        case '*':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.MULEQ
            else:
                lex = Lex.MUL
        case '!':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.NE
            else:
                lex = Lex.NOT
        case '/':
            next_ch()
            if text.ch == '=':  # /=
                next_ch()
                lex = Lex.DIVEQ
            elif text.ch == '/':
                end_of_the_line_comment()  # EndOfTheLineComment
                next_lex()
            elif text.ch == '*':
                traditional_comment()  # TraditionalComment
                next_lex()
            else:  # /
                lex = Lex.DIV
        case '~':
            next_ch()
            lex = Lex.TILDA
        case '&':
            next_ch()
            if text.ch == '=':  # &=
                next_ch()
                lex = Lex.ANDEQ
            elif text.ch == '&':  # &&
                next_ch()
                lex = Lex.ANDAND
            elif text.ch == '^':  # &^
                next_ch()
                if text.ch == '=':  # &^=
                    next_ch()
                    lex = Lex.ANDCARETEQ
                else:
                    lex = Lex.ANDCARET
            else:
                lex = Lex.AND
        case '|':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.OREQ
            elif text.ch == '|':
                next_ch()
                lex = Lex.OROR
            else:
                lex = Lex.OR
        case ':':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.ASS
            else:
                lex = Lex.COLON
        case '^':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.CARETEQ
            else:
                lex = Lex.CARET
        case '%':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.MODEQ
            else:
                lex = Lex.MOD

        # Литералы
        case _ if text.ch in digits:
            if text.ch == '0':
                next_ch()
                if text.ch in '123456789':
                    decimal_digits()
                    if text.ch == '.':
                        next_ch()
                        if text.ch in digits:
                            decimal_digits()
                        if text.ch in 'eE':
                            decimal_exponent()
                        lex = Lex.FLOATLIT
                    else:
                        lex = Lex.INTEGERLIT
                elif text.ch == '_':  # 0_ (decimal_lit или octal_lit)
                    next_ch()
                    if text.ch in digits:
                        decimal_digits()
                    else:
                        error.lexError('Ожидается цифра')
                    lex = Lex.INTEGERLIT
                elif text.ch in 'bB':
                    binary_lit()
                    lex = Lex.INTEGERLIT
                elif text.ch in 'oO':
                    octal_lit()
                    lex = Lex.INTEGERLIT
                elif text.ch in 'xX':
                    next_ch()
                    if text.ch == '.':  # 0x.
                        next_ch()
                        hex_digits()
                        hex_exponent()
                        lex = Lex.FLOATLIT
                    else:  # 0x
                        if text.ch == '_':
                            next_ch()
                        hex_digits()
                        if text.ch == '.':
                            next_ch()
                            if text.ch in hexdigits:
                                hex_digits()
                            hex_exponent()
                            lex = Lex.FLOATLIT
                        elif text.ch in 'pP':
                            hex_exponent()
                            lex = Lex.FLOATLIT
                        else:
                            lex = Lex.INTEGERLIT
                elif text.ch == '.':
                    next_ch()
                    if text.ch in digits:
                        decimal_digits()
                    elif text.ch == '_':
                        error.lexError('_ должен быть между цифрами')
                    if text.ch in 'eE':
                        decimal_exponent()
                    lex = Lex.FLOATLIT
                else:
                    lex = Lex.INTEGERLIT
            else:  # '123456789'
                decimal_digits()
                if text.ch == '.':
                    next_ch()
                    if text.ch in digits:
                        decimal_digits()
                    elif text.ch == '_':
                        error.lexError('_ должен быть между цифрами')
                    if text.ch in 'eE':
                        decimal_exponent()
                    lex = Lex.FLOATLIT
                elif text.ch in 'eE':
                    decimal_exponent()
                    lex = Lex.FLOATLIT
                elif text.ch in 'pP':
                    error.lexError('p экспонента требует шестнадцатеричную мантиссу')
                else:
                    lex = Lex.INTEGERLIT
            if text.ch == 'i':
                next_ch()
                lex = Lex.COMPLEXLIT
        case "'":  # RuneLiteral
            next_ch()
            if text.ch == '\\':
                next_ch()
                if text.ch == 'u':
                    little_u_value()
                elif text.ch == 'U':
                    big_u_value()
                elif text.ch in {'a', 'b', 'f', 'n', 'r', 't', 'v', '\\', '\'', '\"'}:
                    next_ch()
                elif text.ch == 'x':
                    hex_byte_value()
                elif text.ch in octdigits:
                    octal_byte_value()
                else:
                    error.lexError('После \\ ожидается спец.символ')
            if text.ch == "'":
                next_ch()
                lex = Lex.RUNELIT
            else:
                error.lexError('В \'\' кавычках должен быть ЕДИНСТВЕННЫЙ символ')
        case '`':
            next_ch()
            while True:
                if text.ch == '`':
                    next_ch()
                    lex = Lex.STRINGLIT
                    break
                elif text.ch == text.chEOT:
                    error.lexError('Не закончена строка')
                else:
                    next_ch()
        case '"':  # StringLiteral
            next_ch()
            while True:
                if text.ch == '"':
                    next_ch()
                    lex = Lex.STRINGLIT
                    break
                elif text.ch == '\\':
                    next_ch()
                    if text.ch == 'u':
                        little_u_value()
                    elif text.ch == 'U':
                        big_u_value()
                    elif text.ch in {'a', 'b', 'f', 'n', 'r', 't', 'v', '\\', '\'', '\"'}:
                        next_ch()
                    elif text.ch == 'x':
                        hex_byte_value()
                    else:
                        error.lexError('После \\ ожидается спец.символ')
                elif text.ch == text.chEOT:
                    error.lexError('Не закончена строка')
                else:
                    next_ch()

        case text.chEOT:
            lex = Lex.EOT
        case _:
            error.lexError("Недопустимый символ")
