# Данный модуль содержит лексический анализатор

from enum import Enum
from string import octdigits, hexdigits

import Errors
from Text import next_ch
import Text
from Base import *
class Lex(Enum):
        ALIGNAS, ALIGNOF, AND, AND_EQ, ASM, AUTO, BITAND, BITOR, BOOL, BREAK, \
        CASE, CATCH, CHAR, CHAR8_T, CHAR16_T, CHAR32_T, CLASS, COMPL, CONCEPT, \
        CONST, CONST_CAST, CONSTEVAL, CONSTEXPR, CONSTINIT, CONTINUE, CO_AWAIT, \
        CO_RETURN, CO_YIELD, DECLTYPE, DEFAULT, DELETE, DO, DOUBLE, DYNAMIC_CAST, \
        ELSE, ENUM, EXPLICIT, EXPORT, EXTERN, FALSE, FLOAT, FOR, FRIEND, GOTO, IF, INLINE, \
        INT, LONG, MUTABLE, NAMESPACE, NEW, NOEXCEPT, NOT, NOT_EQ, NULLPTR, OPERATOR, OR, \
        OR_EQ, PRIVATE, PROTECTED, PUBLIC, REGISTER, REINTERPRET_CAST, REQUIRES, RETURN, \
        SHORT, SIGNED, SIZEOF, STATIC, STATIC_ASSERT, STATIC_CAST, STRING, STRUCT, SWITCH, TEMPLATE, \
        THIS, THREAD_LOCAL, THROW, TRUE, TRY, TYPEDEF, TYPEID, TYPENAME, UNION, UNSIGNED, \
        USING, VIRTUAL, VOID, VOLATILE, WCHAR_T, WHILE, XOR, XOR_EQ = range(93)



lex_names = []
for enum_lex in Lex:
        lex_names.append(enum_lex.name)
lex_dict = dict(zip(lex_names, [0] * len(Lex)))
name = ''


keywords = {
        'alignas': Lex.ALIGNAS,
        'alignof': Lex.ALIGNOF,
        'and': Lex.AND,
        'and_eq': Lex.AND_EQ,
        'asm': Lex.ASM,
        'auto': Lex.AUTO,
        'bitand': Lex.BITAND,
        'bitor': Lex.BITOR,
        'bool': Lex.BOOL,
        'break': Lex.BREAK,
        'case': Lex.CASE,
        'catch': Lex.CATCH,
        'char': Lex.CHAR,
        'char8_t': Lex.CHAR8_T,
        'char16_t': Lex.CHAR16_T,
        'char32_t': Lex.CHAR32_T,
        'class': Lex.CLASS,
        'compl': Lex.COMPL,
        'concept': Lex.CONCEPT,
        'const': Lex.CONST,
        'const_cast': Lex.CONST_CAST,
        'consteval': Lex.CONSTEVAL,
        'constexpr': Lex.CONSTEXPR,
        'constint': Lex.CONSTINIT,
        'continue': Lex.CONTINUE,
        'co_await': Lex.CO_AWAIT,
        'co_return': Lex.CO_RETURN,
        'co_yield': Lex.CO_YIELD,
        'decl_type': Lex.DECLTYPE,
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
        'noexcept': Lex.NOEXCEPT,
        'not': Lex.NOT,
        'not_eq': Lex.NOT_EQ,
        'nullptr': Lex.NULLPTR,
        'operator': Lex.OPERATOR,
        'or': Lex.OR,
        'or_eq': Lex.OR_EQ,
        'private': Lex.PRIVATE,
        'protected': Lex.PROTECTED,
        'public': Lex.PUBLIC,
        'register': Lex.REGISTER,
        'reinterpret_cast': Lex.REINTERPRET_CAST,
        'requires': Lex.REQUIRES,
        'return': Lex.RETURN,
        'short': Lex.SHORT,
        'signed': Lex.SIGNED,
        'sizeof': Lex.SIZEOF,
        'static': Lex.STATIC,
        'static_assert': Lex.STATIC_ASSERT,
        'static_cast': Lex.STATIC_CAST,
        'struct': Lex.STRUCT,
        'string': Lex.STRING,
        'switch': Lex.SWITCH,
        'template': Lex.TEMPLATE,
        'this': Lex.THIS,
        'thread_local': Lex.THREAD_LOCAL,
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
        'wchar_t': Lex.WCHAR_T,
        'while': Lex.WHILE,
        'xor': Lex.XOR,
        'xor_eq': Lex.XOR_EQ,
}


def integer_sign():
    if Text.ch in sign:
        next_ch()
    if Text.ch in digits:
        next_ch()
        while Text.ch in digits:
            next_ch()
    else:
        Errors.lexError('Ожидается десятичное число')



def octal_escape():
    first_ch = Text.ch
    next_ch()
    if Text.ch in octdigits:
        next_ch()
        if Text.ch in octdigits:
            if first_ch in '0123':
                next_ch()
            else:
                Errors.lexError('Первая цифра должна быть от 0 до 3')


def escape_seq():
    next_ch()
    if Text.ch in 'btnfr\"\'\\': #backspace, tab, new line, form feed, carriage return
        next_ch()
    elif Text.ch in octdigits:
        octal_escape()
    else:
        Errors.lexError('Недопустимый символ после \\')


def traditional_comment():
    next_ch()
    while True:
        if Text.ch == '*':
            next_ch()
            if Text.ch == '/':
                next_ch()
                break
        elif Text.ch == Text.chEOT:
            Errors.lexError('Незаконченный комментарий')
        else:
            next_ch()


def end_of_the_line_comment():
    next_ch()
    while Text.ch not in {Text.chEOL, Text.chEOT}:
        next_ch()




#ВОТ ТУТ МНОГО ИСПРАВЛЯТЬ
def next_lex():
    global name
    while Text.ch in {Text.chSPACE, Text.chHT, Text.chEOL, Text.chFF}:
        next_ch()
    match Text.ch:

        # Идентификаторы
        case _ if Text.ch in cpp_letter:
            name = Text.ch
            next_ch()
            while Text.ch in cpp_letter_or_digit:
                name += Text.ch
                next_ch()
            return keywords.get(name, Lex.NAME)

        # Литералы
        case _ if Text.ch in digits:
            if Text.ch == '0':
                next_ch()
                if Text.ch in 'xX':
                    next_ch()
                    if Text.ch in hexdigits:
                        next_ch()
                    else:
                        Errors.lexError('Ожидается шестнадцатеричная цифра')
                    while Text.ch in hexdigits:
                        next_ch()
                elif Text.ch in octdigits:
                    next_ch()
                    while Text.ch in octdigits:
                        next_ch()
                    if Text.ch in '89':
                        next_ch()
                        while Text.ch in digits:
                            next_ch()
                        if Text.ch not in '.eEfFdD':
                            Errors.lexError('Ожидается \'.\', экспонента или суффикс типа')
            while Text.ch in digits:
                next_ch()
            if Text.ch == '.':
                next_ch()
                while Text.ch in digits:
                    next_ch()
                if Text.ch in exponent_indicator:
                    next_ch()
                    integer_sign()
                if Text.ch in float_type_suffix:
                    if Text.ch in 'fF':
                        next_ch()
                        return Lex.FLOAT
                    else:
                        next_ch()
                return Lex.DOUBLE
            elif Text.ch in exponent_indicator:
                next_ch()
                integer_sign()
                if Text.ch in float_type_suffix:
                    if Text.ch in 'fF':
                        next_ch()
                        return Lex.FLOAT
                    else:
                        next_ch()
                return Lex.DOUBLE
            elif Text.ch in float_type_suffix:
                if Text.ch in 'fF':
                    next_ch()
                    return Lex.FLOAT
                else:
                    next_ch()
                return Lex.DOUBLE
            else:
                if Text.ch in integer_type_suffix:
                    next_ch()
                return Lex.INT
        case '"':  # StringLiteral
            next_ch()
            while True:
                if Text.ch == '"':
                    next_ch()
                    return Lex.STRING
                elif Text.ch == '\\':
                    escape_seq()
                elif Text.ch == Text.chEOT:
                    Errors.lexError('Не закончена строка')
                else:
                    next_ch()
        case "'":  # CharacterLiteral
            next_ch()
            if Text.ch == '\\':
                escape_seq()
            else:
                next_ch()
            if Text.ch == "'":
                next_ch()
                return Lex.CHAR
            else:
                Errors.lexError('В \'\' кавычках должен быть ЕДИНСТВЕННЫЙ символ')

        # Разделители
        case '(':
            next_ch()
            return Lex.LPAR
        case ')':
            next_ch()
            return Lex.RPAR
        case '{':
            next_ch()
            return Lex.BEGIN
        case '}':
            next_ch()
            return Lex.END
        case '[':
            next_ch()
            return Lex.LSQ
        case ']':
            next_ch()
            return Lex.RSQ
        case ';':
            next_ch()
            return Lex.SEMI
        case ',':
            next_ch()
            return Lex.COMMA
        case '.':
            next_ch()
            if Text.ch in digits:  # Digits
                next_ch()
                while Text.ch in digits:
                    next_ch()
                if Text.ch in exponent_indicator:  # ExponentPart
                    next_ch()
                    integer_sign()
                if Text.ch in float_type_suffix:
                    if Text.ch in 'fF':
                        next_ch()
                        return Lex.FLOATINGNUMBER
                    else:
                        next_ch()
                return Lex.DOUBLENUMBER
            else:
                return Lex.DOT

        # Операции
        case '=':
            next_ch()
            if Text.ch == '=':
                next_ch()
                return Lex.EQEQ
            else:
                return Lex.EQ
        case '+':
            next_ch()
            if Text.ch == '=':
                next_ch()
                return Lex.PLUSEQ
            elif Text.ch == '+':
                next_ch()
                return Lex.INC
            else:
                return Lex.PLUS
        case '>':
            next_ch()
            if Text.ch == '=':
                next_ch()
                return Lex.GE
            elif Text.ch == '>':
                next_ch()
                if Text.ch == '=':
                    next_ch()
                    return Lex.GTGE
                elif Text.ch == '>':
                    next_ch()
                    if Text.ch == '=':
                        next_ch()
                        return Lex.GTGTGE
                    else:
                        return Lex.GTGTGT
                else:
                    return Lex.GTGT
            else:
                return Lex.GT
        case '<':
            next_ch()
            if Text.ch == '=':
                next_ch()
                return Lex.LE
            elif Text.ch == '<':
                next_ch()
                if Text.ch == '=':
                    next_ch()
                    return Lex.LTLE
                else:
                    return Lex.LTLT
            else:
                return Lex.LT
        case '-':
            next_ch()
            if Text.ch == '=':
                next_ch()
                return Lex.MINUSEQ
            elif Text.ch == '-':
                next_ch()
                return Lex.DEC
            else:
                return Lex.MINUS
        case '*':
            next_ch()
            if Text.ch == '=':
                next_ch()
                return Lex.MULTEQ
            else:
                return Lex.MULT
        case '!':
            next_ch()
            if Text.ch == '=':
                next_ch()
                return Lex.NOTEQ
            else:
                return Lex.NOT
        case '/':
            next_ch()
            if Text.ch == '=':
                next_ch()
                return Lex.DIVEQ
            elif Text.ch == '/':
                end_of_the_line_comment()  # EndOfTheLineComment
                return next_lex()
            elif Text.ch == '*':
                traditional_comment()  # TraditionalComment
                return next_lex()
            else:
                return Lex.DIV
        case '~':
            next_ch()
            return Lex.TILDE
        case '&':
            next_ch()
            if Text.ch == '=':
                next_ch()
                return Lex.ANDEQ
            elif Text.ch == '&':
                next_ch()
                return Lex.AND
            else:
                return Lex.BITAND
        case '?':
            next_ch()
            return Lex.TERN
        case '|':
            next_ch()
            if Text.ch == '=':
                next_ch()
                return Lex.OREQ
            elif Text.ch == '|':
                next_ch()
                return Lex.OR
            else:
                return Lex.BITOR
        case ':':
            next_ch()
            return Lex.COLON
        case '^':
            next_ch()
            if Text.ch == '=':
                next_ch()
                return Lex.CARETEQ
            else:
                return Lex.CARET
        case '%':
            next_ch()
            if Text.ch == '=':
                next_ch()
                return Lex.MODEQ
            else:
                return Lex.MOD
        case Text.chEOT:
            return Lex.EOT
        case _:
            Errors.lexError("Недопустимый символ")