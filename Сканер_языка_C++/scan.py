# Лексический анализатор C++
from enum import Enum

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
    CATCH, CHAR, CLASS, COMPL, CONST, CONSTCAST, EXPORT, EXTERN, FALSE, FLOAT, FOR, FRIEND,
    NOTEQ, OPERATOR, OR, OREQ, PRIVATE, PROTECTED, STRUCT, SWITCH, TEMPLATE, THIS, THROW, TRUE,
    VOLATILE, WCHART, WHILE, XOR, XOREQ,

    BEGIN, END, LSQPAR, RSQPAR, GRID, DOUBLEGRID, LPAR, RPAR, LTCOLON, GTCOLON, LTMOD, GTMOD, MODCOLON,
    DOUBLEMODCOLON, SEMI, COLON, QUESTIONSIGN, DOUBLECOLON, DOT, DOTMUL, PLUS, MINUS, MUL, DIV, MOD, CARET,
    TILDA, EQ, LT, GT, PLUSEQ, MINUSEQ, MULEQ, DIVEQ, MODEQ, CARETEQ, ORSIGNEQ, LTLTEQ, GTGTEQ, LTLT, GTGT,
    EQEQ, LTEQ, GTEQ, ANDAND, OROR, INC, DEC, COMMA, ARROW, ARROWMUL, THREEDOT, COMP,

    IDENTIFIER, EOT,
    INTEGERLIT, CHARACTER, FLOATLIT, STRING) = range(133)



lex_names = []
for enum_lex in Lex:
    lex_names.append(enum_lex.name)
lex_dict = dict(zip(lex_names, [0] * len(Lex)))
name = ''



keywords = {
    'and': Lex.AND,
    'and_eq': Lex.ANDEQ,
    'asm': Lex.ASM,
    'auto': Lex.AUTO,
    'bitand': Lex.BITAND,
    'bitor': Lex.BITOR,
    'bool': Lex.BOOL,
    'break': Lex.BREAK,
    'case': Lex.CASE,
    'catch': Lex.CATCH,
    'char': Lex.CHAR,
    'class': Lex.CLASS,
    'compl': Lex.COMPL,
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
    'or': Lex.OR,
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
    'xor': Lex.XOR,
    'xor_eq': Lex.XOREQ
}

def traditional_comment():
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

def end_of_the_line_comment():
    next_ch()
    while text.ch not in {text.chEOL, text.chEOT}:
        next_ch()


def signed_integer():
    if text.ch in sign:
        next_ch()
    if text.ch in digit:
        next_ch()
        while text.ch in digit:
            next_ch()
    else:
        error.lexError('Ожидается десятичное число')

def octal_escape():
    first_ch = text.ch
    next_ch()
    if text.ch in octal_digit:
        next_ch()
        if text.ch in octal_digit:
            if first_ch in '0123':
                next_ch()
            else:
                error.lexError('Первая цифра после \\ должна быть от 0 до 3')

def escape_sequence():
    next_ch()
    if text.ch in '\"\'\\':
        next_ch()
    elif text.ch in octal_digit:
        octal_escape()
    else:
        error.lexError('Недопустимый символ после \\')




def next_lex():
    global name, lex
    while text.ch in {text.chSPACE, text.chHT, text.chFF, text.chEOL}:
        next_ch()
    match text.ch:

        # Идентификаторы и служебные слова
        case _ if text.ch in non_digit + '\\' : # !!! _a..zA..Z \uDDDD  \UDDDDDDDD

            name = text.ch
            next_ch()
            while text.ch in non_digit + digit:  # !!!!!
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
                return Lex.GTCOLON
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
            if text.ch == '.':
                next_ch()
                if text.ch == '.':
                    next_ch()
                    return Lex.THREEDOT # ...
                else:
                    error.lexError('Должно быть три точки')
            elif text.ch == '*':
                next_lex()
                return Lex.DOTMUL # .*
            else:
                return Lex.DOT
        case '?':
            next_ch()
            return Lex.QUESTIONSIGN  # ?
        case '+':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.PLUSEQ # +=
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
                end_of_the_line_comment()  # EndOfTheLineComment
                return next_lex()
            elif text.ch == '*':
                traditional_comment()  # TraditionalComment
                return next_lex()
            else:
                return Lex.DIV # /
        case '%':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.MODEQ
            elif text.ch == '>':  # %>
                next_ch()
                return Lex.GTMOD
            elif text.ch == ':':
                next_ch()
                if text.ch == '%':
                    next_ch()
                    if text.ch == ':':
                        next_ch()
                        return Lex.DOUBLEMODCOLON  # %:%:
                else:
                    return Lex.MODCOLON  # %:
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
                return Lex.ANDEQ # &=
            elif text.ch == '&':
                next_ch()
                return Lex.ANDAND # &&
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
                else:  # <<
                    return Lex.LTLT  # <<
            elif text.ch == ':':
                next_ch()
                return Lex.LTCOLON  # <:
            elif text.ch == '%':
                next_ch()
                return Lex.LTMOD  # <%
            else:
                return Lex.LT  # <
        case '>':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.GTEQ # >=
            elif text.ch == '>':
                next_ch()
                if text.ch == '=':
                    next_ch()
                    return Lex.GTGTEQ # >>=
                else:  # >>
                    return Lex.GTGT # >>
            else:
                return Lex.GT # >

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
                elif text.ch in octal_digit:
                    next_ch()
                    while text.ch in octal_digit:
                        next_ch()
                    if text.ch in '89':
                        next_ch()
                        while text.ch in digit:
                            next_ch()
                        if text.ch not in '.eEfFdD':
                            error.lexError('Ожидается \'.\', экспонента или суффикс типа')
            while text.ch in digit:
                next_ch()
            if text.ch == '.':
                next_ch()
                while text.ch in digit:
                    next_ch()
                if text.ch in exponent_part:
                    next_ch()
                    signed_integer()
                if text.ch in float_suffix:
                    if text.ch in 'fF':
                        next_ch()
                        return Lex.FLOATLIT
                    else:
                        next_ch()
                # return Lex.DOUBLENUMBER
            elif text.ch in exponent_part:
                next_ch()
                signed_integer()
                if text.ch in float_suffix:
                    if text.ch in 'fF':
                        next_ch()
                        return Lex.FLOATLIT
                    else:
                        next_ch()
                # return Lex.DOUBLENUMBER
            elif text.ch in float_suffix:
                if text.ch in 'fF':
                    next_ch()
                    return Lex.FLOATLIT
                else:
                    next_ch()
                # return Lex.DOUBLENUMBER
            else:
                if text.ch in integer_suffix:
                    next_ch()
                return Lex.INTEGERLIT
        case '"':  # StringLiteral
            next_ch()
            while True:
                if text.ch == '"':
                    next_ch()
                    return Lex.STRING
                elif text.ch == '\\':
                    escape_sequence()
                elif text.ch == text.chEOT:
                    error.lexError('Не закончена строка')
                else:
                    next_ch()
        case "'":  # CharacterLiteral
            next_ch()
            if text.ch == '\\':
                escape_sequence()
            else:
                next_ch()
            if text.ch == "'":
                next_ch()
                return Lex.CHARACTER
            else:
                error.lexError('В \'\' кавычках должен быть ЕДИНСТВЕННЫЙ символ')



        case text.chEOT:
            return Lex.EOT
        case _:
            error.lexError("Недопустимый символ")