# Лексический анализатор C++
from enum import Enum

import error
from text import next_ch
import text
from sets import *


class Lex(Enum):
    (AND, ANDEQ, ASM, AUTO, BOOL, BREAK, CASE,
    CONTINUE, DEFAULT, DELETE, DO, DOUBLE, DYNAMIC_CAST, ELSE, ENUM, EXPLICIT,
    GOTO, IF, INLINE, INT, LONG, MUTABLE, NAMESPACE, NEW, NOT,
    PUBLIC, REGISTER, REINTERPRETCAST, RETURN, SHORT, SIGNED, SIZEOF, STATIC, STATICCAST,
    TRY, TYPEDEF, TYPEID, TYPENAME, UNION, UNSIGNED, USING, VIRTUAL, VOID,
    CATCH, CHAR, CLASS, CONST, CONSTCAST, EXPORT, EXTERN, FALSE, FLOAT, FOR, FRIEND,
    NOTEQ, OPERATOR, OR, OREQ, PRIVATE, PROTECTED, STRUCT, SWITCH, TEMPLATE, THIS, THROW, TRUE,
    VOLATILE, WCHART, WHILE, COMP,

    BEGIN, END, LSQPAR, RSQPAR, GRID, DOUBLEGRID, LPAR, RPAR, LTCOLON, GTCOLON, LTMOD,
    SEMI, COLON, DOUBLECOLON, DOT, POINTER_DEFERENCING, PLUS, MINUS, MUL, DIV, MOD, CARET,
    TILDA, EQ, LT, GT, PLUSEQ, MINUSEQ, MULEQ, DIVEQ, MODEQ, CARETEQ, ORSIGNEQ, LTLTEQ, GTGTEQ, LTLT, GTGT,
    EQEQ, LTEQ, GTEQ, ANDAND, OROR, INC, DEC, COMMA, ARROW, ARROWMUL, THREEDOT, BACKSLASH,

    IDENTIFIER, EOT, INTEGER_LIT, CHARACTER, STRING, FLOAT_LIT, DOUBLE_LIT, LONG_DOUBLE_LIT) = range(127)



lex_names = []
for enum_lex in Lex:
    lex_names.append(enum_lex.name)
lex_dict = dict(zip(lex_names, [0] * len(Lex)))
name = ''



keywords = {
    'and': Lex.ANDAND,
    'and_eq': Lex.ANDEQ,
    'asm': Lex.ASM,
    'auto': Lex.AUTO,
    'bitand': Lex.AND,
    'bitor': Lex.OR,
    'bool': Lex.BOOL,
    'break': Lex.BREAK,
    'case': Lex.CASE,
    'catch': Lex.CATCH,
    'char': Lex.CHAR,
    'class': Lex.CLASS,
    'compl': Lex.TILDA,
    'const': Lex.CONST,
    'const_cast': Lex.CONSTCAST,
    'comp': Lex.COMP,
    'continue': Lex.CONTINUE,
    'default': Lex.DEFAULT,
    'delete': Lex.DELETE,
    'do': Lex.DO,
    'double': Lex.DOUBLE,
    'dynamic_cast': Lex.DYNAMIC_CAST,
    'else': Lex.ELSE,
    'enum': Lex.ENUM,
    'explicit': Lex.EXPLICIT,
    'export': Lex.EXPORT,
    'extern': Lex.EXTERN,
    'false': Lex.FALSE,
    'float': Lex.FLOAT,
    'for': Lex.FOR,
    'friend': Lex.FRIEND,
    'goto': Lex.GOTO,
    'if': Lex.IF,
    'inline': Lex.INLINE,
    'int': Lex.INT,
    'long': Lex.LONG,
    'mutable': Lex.MUTABLE,
    'namespace': Lex.NAMESPACE,
    'new': Lex.NEW,
    'not': Lex.NOT,
    'not_eq': Lex.NOTEQ,
    'operator': Lex.OPERATOR,
    'or': Lex.OROR,
    'or_eq': Lex.OREQ,
    'private': Lex.PRIVATE,
    'protected': Lex.PROTECTED,
    'public': Lex.PUBLIC,
    'register': Lex.REGISTER,
    'reinterpret_cast': Lex.REINTERPRETCAST,
    'return': Lex.RETURN,
    'short': Lex.SHORT,
    'signed': Lex.SIGNED,
    'sizeof': Lex.SIZEOF,
    'static': Lex.STATIC,
    'static_cast': Lex.STATICCAST,
    'struct': Lex.STRUCT,
    'switch': Lex.SWITCH,
    'template': Lex.TEMPLATE,
    'this': Lex.THIS,
    'throw': Lex.THROW,
    'true': Lex.TRUE,
    'try': Lex.TRY,
    'typedef': Lex.TYPEDEF,
    'typeid': Lex.TYPEID,
    'typename': Lex.TYPENAME,
    'union': Lex.UNION,
    'unsigned': Lex.UNSIGNED,
    'using': Lex.USING,
    'virtual': Lex.VIRTUAL,
    'void': Lex.VOID,
    'volatile': Lex.VOLATILE,
    'wchar_t': Lex.WCHART,
    'while': Lex.WHILE,
    'xor': Lex.CARET,
    'xor_eq': Lex.CARETEQ
}


def unicode_character_name():
    next_ch()
    if text.ch == 'u':
        next_ch()
        unicode = ''
        for _ in range(4):
            if text.ch in hexadecimal_digit:
                unicode += text.ch
                next_ch()
            else:
                error.lexError('UCN дописан не до конца')
        if int(unicode, 16) in range(55296, 57344): #0xD000 - 0xDFFF
            error.lexError('Недопустимое значение UCN')
        else:
            return chr(int(unicode, 16))
    elif text.ch == 'U':
        next_ch()
        unicode = ''
        for _ in range(8):
            if text.ch in hexadecimal_digit:
                unicode += text.ch
                next_ch()
            else:
                error.lexError('UCN дописан не до конца')
        if int(unicode, 16) in range(55296, 57344): #0xD000 - 0xDFFF
            error.lexError('Недопустимое значение UCN')
        else:
            return chr(int(unicode, 16))
    else:
        error.lexError('Ожидается u или U после \'\\\' (universal-character-name)')


def multiline_comment():
    next_ch()
    while True:
        if text.ch == '*':
            next_ch()
            if text.ch == '/':
                next_ch()
                break
        elif text.ch == text.chEOT:
            error.lexError('Не закончен комментарий')
        else:
            next_ch()


def single_line_comment():
    next_ch()
    while text.ch not in {text.chEOL, text.chEOT}:
        next_ch()


def signed_int():
    if text.ch in sign:
        next_ch()
    if text.ch in digit:
        next_ch()
        while text.ch in digit:
            next_ch()
    else:
        error.lexError('Ожидается десятичное число')


def octal_escape_sequence():
    next_ch()
    if text.ch in octal_digit:
        next_ch()
        if text.ch in octal_digit:
            next_ch()
            if text.ch in digit + non_digit:
                error.lexError('Octal-escape-sequence может состоять не более чем из ТРЕХ ВОСЬМЕРИЧНЫХ ЦИФР')


def hexadecimal_escape_sequence():
    next_ch()
    if text.ch in hexadecimal_digit:
        while text.ch in hexadecimal_digit:
            next_ch()
    else:
        error.lexError('Ожидается шестнадцатеричная цифра')


def escape_sequence():
    universal_character_name = ''
    next_ch()
    if text.ch in '\"\'?abfnrtv':
        next_ch()
    elif text.ch in octal_digit:
        octal_escape_sequence()
    elif text.ch == 'x':
        hexadecimal_escape_sequence()
    elif text.ch == 'u':
        next_ch()
        universal_character_name = ''
        for _ in range(4):
            if text.ch in hexadecimal_digit:
                universal_character_name += text.ch
                next_ch()
            else:
                error.lexError('UCN дописан не до конца')
        if int(universal_character_name, 16) in range(55296, 57344):
            error.lexError('Недопустимое значение UCN')
        else:
            return chr(int(universal_character_name, 16))
    elif text.ch == 'U':
        next_ch()
        unicode = ''
        for _ in range(8):
            if text.ch in hexadecimal_digit:
                unicode += text.ch
                next_ch()
            else:
                error.lexError('UCN дописан не до конца')
        if int(unicode, 16) in range(55296, 57344):
            error.lexError('Недопустимое значение UCN')
        else:
            return chr(int(unicode, 16))
    elif text.ch == text.chEOL:
        next_ch()
    else:
        error.lexError('Недопустимый символ после \\')


def next_lex():
    global name
    while text.ch in {text.chSPACE, text.chHT, text.chFF, text.chEOL}:
        next_ch()
    match text.ch:

        # Идентификаторы и служебные слова
        case 'L':
            next_ch()
            if text.ch == "'":
                next_ch()
                while True:
                    if text.ch == "'":
                        next_ch()
                        return Lex.CHARACTER
                    elif text.ch == '\\':
                        escape_sequence()
                    elif text.ch == text.chEOT:
                        error.lexError('Неправильно написан character-literal')
                    # elif text.ch == text.chEOL:
                    #     error.lexError('Неправильно написан character-literal')
                    elif text.ch == "'":
                        error.lexError('Внутри character-literal не должен встречаться символ одинарной кавычки')
                    else:
                        next_ch()
            elif text.ch == '"':
                next_ch()
                while True:
                    if text.ch == '"':
                        next_ch()
                        return Lex.STRING
                    elif text.ch == '\\':
                        escape_sequence()
                    elif text.ch == text.chEOT:
                        error.lexError('Не закончена строка')
                    # elif text.ch == text.chEOL:
                    #     error.lexError('Не закончена строка')
                    elif text.ch == '"':
                        error.lexError('Внутри строки не должен встречаться символ двойной кавычки')
                    else:
                        next_ch()
            elif text.ch in non_digit + digit:
                name = 'L' + text.ch
                next_ch()
                while text.ch in non_digit + digit:
                    name += text.ch
                    next_ch()
                return keywords.get(name, Lex.IDENTIFIER)
            else:
                return Lex.IDENTIFIER
        case _ if text.ch in non_digit + '\\':
            if text.ch == '\\':
                name = unicode_character_name()
            else:
                name = text.ch
                next_ch()
            while text.ch in non_digit + '\\' + digit:
                if text.ch == '\\':
                    name += unicode_character_name()
                else:
                    name += text.ch
                    next_ch()
            return keywords.get(name, Lex.IDENTIFIER)

        # Операции и разделители
        case '{':
            next_ch()
            return Lex.BEGIN
        case '}':
            next_ch()
            return Lex.END
        case '[':
            next_ch()
            return Lex.LSQPAR
        case ']':
            next_ch()
            return Lex.RSQPAR
        case '#': # #
            next_ch()
            if text.ch == '#': # ##
                next_ch()
                return Lex.DOUBLEGRID
            else:
                return Lex.GRID
        case '(':
            next_ch()
            return Lex.LPAR
        case ')':
            next_ch()
            return Lex.RPAR
        case ';':
            next_ch()
            return Lex.SEMI
        case ':':
            next_ch()
            if text.ch == '>':  # :>
                next_ch()
                return Lex.RSQPAR
            elif text.ch == ':':
                next_ch()
                return Lex.DOUBLECOLON  # ::
            else:
                return Lex.COLON
        case ',':
            next_ch()
            return Lex.COMMA
        case '.':
            next_ch()
            if text.ch in digit:
                next_ch()
                while text.ch in digit:
                    next_ch()
                if text.ch in exponent_part:
                    next_ch()
                    signed_int()
                if text.ch in float_or_double_suffix:
                    if text.ch in float_suffix:
                        next_ch()
                        return Lex.FLOAT_LIT
                    elif text.ch in long_suffix:
                        next_ch()
                        return Lex.LONG_DOUBLE_LIT
                else:
                    return Lex.DOUBLE_LIT
            elif text.ch == '.':
                next_ch()
                if text.ch == '.':
                    next_ch()
                    return Lex.THREEDOT  # ...
                else:
                    error.lexError('Должно быть три точки')
            elif text.ch == '*':
                next_lex()
                return Lex.POINTER_DEFERENCING # .*
            else:
                return Lex.DOT
        # Триграфы:
        case '?':
            next_ch()
            if text.ch == '?':
                next_ch()
                if text.ch == '=':
                    next_ch()
                    return Lex.GRID
                elif text.ch == '/':
                    next_ch()
                    return Lex.BACKSLASH
                elif text.ch == '\'':
                    next_ch()
                    return Lex.CARET
                elif text.ch == '(':
                    next_ch()
                    return Lex.LSQPAR
                elif text.ch == ')':
                    next_ch()
                    return Lex.RSQPAR
                elif text.ch == '!':
                    next_ch()
                    return Lex.OR
                elif text.ch == '<':
                    next_ch()
                    return Lex.BEGIN
                elif text.ch == '>':
                    next_ch()
                    return Lex.END
                elif text.ch == '-':
                    next_ch()
                    return Lex.TILDA
                else:
                    error.lexError('Ошибка в написании триграфа')
            else:
                error.lexError('Ошибка в написании триграфа')

        # # Перевод (разрыв) строки
        # case '\\':
        #     next_ch()
        #     if text.ch == text.chEOL:
        #         next_ch()



        case '+':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.PLUSEQ  # +=
            elif text.ch == '+':
                next_ch()
                return Lex.INC # ++
            else:
                return Lex.PLUS
        case '-':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.MINUSEQ
            elif text.ch == '-':
                next_ch()
                return Lex.DEC
            elif text.ch == '>':
                next_ch()
                if text.ch == '*':
                    next_ch()
                    return Lex.ARROWMUL
                else:
                    return Lex.ARROW
            else:
                return Lex.MINUS
        case '*':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.MULEQ
            else:
                return Lex.MUL
        case '/':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.DIVEQ  # /=
            elif text.ch == '/':
                single_line_comment()
                return next_lex()
            elif text.ch == '*':
                multiline_comment()
                return next_lex()
            else:
                return Lex.DIV  # /
        case '%':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.MODEQ
            elif text.ch == '>':  # %>
                next_ch()
                return Lex.END
            elif text.ch == ':':
                next_ch()
                if text.ch == '%':
                    next_ch()
                    if text.ch == ':':
                        next_ch()
                        return Lex.DOUBLEGRID  # %:%:
                else:
                    return Lex.GRID  # %:
            else:
                return Lex.MOD
        case '^':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.CARETEQ
            else:
                return Lex.CARET
        case '&':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.ANDEQ  # &=
            elif text.ch == '&':
                next_ch()
                return Lex.ANDAND  # &&
            else:
                return Lex.AND
        case '|':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.OREQ
            elif text.ch == '|':
                next_ch()
                return Lex.OROR
            else:
                next_ch()
                return Lex.OR
        case '~':
            next_ch()
            return Lex.TILDA
        case '!':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.NOTEQ
            else:
                next_ch()
                return Lex.NOT
        case '=':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.EQEQ  # ==
            else:
                next_ch()
                return Lex.EQ
        case '<':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.LTEQ  # <=
            elif text.ch == '<':
                next_ch()
                if text.ch == '=':
                    next_ch()
                    return Lex.LTLTEQ  # <<=
                else:
                    return Lex.LTLT  # <<
            elif text.ch == ':':
                next_ch()
                return Lex.LSQPAR  # <:
            elif text.ch == '%':
                next_ch()
                return Lex.BEGIN  # <%
            else:
                return Lex.LT  # <
        case '>':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.GTEQ  # >=
            elif text.ch == '>':
                next_ch()
                if text.ch == '=':
                    next_ch()
                    return Lex.GTGTEQ  # >>=
                else:
                    return Lex.GTGT  # >>
            else:
                return Lex.GT  # >

        # Литералы
        case _ if text.ch in digit:
            if text.ch == '0':
                next_ch()
                if text.ch in 'xX':
                    next_ch()
                    if text.ch in hexadecimal_digit:
                        next_ch()
                    else:
                        error.lexError('Ожидается шестнадцатеричная цифра')
                    while text.ch in hexadecimal_digit:
                        next_ch()
                    if text.ch == '.':
                        error.lexError('Ожидается шестнадцатеричная цифра')
                elif text.ch in octal_digit:
                    next_ch()
                    while text.ch in octal_digit:
                        next_ch()
                    if text.ch in '89':
                        error.lexError('Ожидается восьмеричная цифра')
                elif text.ch in digit:
                    next_ch()
                    while text.ch in digit:
                        next_ch()
            while text.ch in digit:
                next_ch()
            if text.ch == '.':
                next_ch()
                while text.ch in digit:
                    next_ch()
                if text.ch in exponent_part:
                    next_ch()
                    signed_int()
                if text.ch in float_or_double_suffix:
                    if text.ch in float_suffix:
                        next_ch()
                        return Lex.FLOAT_LIT
                    elif text.ch in long_suffix:
                        next_ch()
                        return Lex.LONG_DOUBLE_LIT
                else:
                    return Lex.DOUBLE_LIT

            elif text.ch in exponent_part:
                next_ch()
                signed_int()
                if text.ch in float_or_double_suffix:
                    if text.ch in float_suffix:
                        next_ch()
                        return Lex.FLOAT_LIT
                    elif text.ch in long_suffix:
                        next_ch()
                        return Lex.LONG_DOUBLE_LIT
                else:
                    return Lex.DOUBLE_LIT

            else:
                if text.ch in integer_suffix:
                    if text.ch in unsigned_suffix:
                        next_ch()
                        if text.ch in long_suffix:
                            next_ch()
                            return Lex.INTEGER_LIT
                        else:
                            return Lex.INTEGER_LIT
                    elif text.ch in long_suffix:
                        next_ch()
                        if text.ch in unsigned_suffix:
                            next_ch()
                            return Lex.INTEGER_LIT
                        else:
                            return Lex.INTEGER_LIT
                else:
                    return Lex.INTEGER_LIT

        case '"':  # STRING
            next_ch()
            while True:
                if text.ch == '"':
                    next_ch()
                    while text.ch in {text.chEOL, text.chSPACE}:
                        next_ch()
                    if text.ch == '"':
                        return next_lex()
                    else:
                        return Lex.STRING
                elif text.ch == '\\':
                    escape_sequence()
                elif text.ch == text.chEOT:
                    error.lexError('Не закончена строка')
                elif text.ch == '"':
                    error.lexError('Внутри строки не должен встречаться символ символ \' " \'')
                else:
                    next_ch()

        case "'":  # CHARACTER
            next_ch()
            while True:
                if text.ch == "'":
                    next_ch()
                    return Lex.CHARACTER
                elif text.ch == '\\':
                    escape_sequence()
                elif text.ch == text.chEOT:
                    error.lexError('Не закончен character-literal')
                # elif text.ch == text.chEOL:
                #     error.lexError('Не закончен character-literal')
                elif text.ch == "'":
                    error.lexError('Внутри character-literal не должен встречаться символ " \' "')
                else:
                    next_ch()

        case text.chEOT:
            return Lex.EOT
        case _:
            error.lexError("Недопустимый символ")
