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
    while text.ch in {text.chSPACE, text.chHT, text.chFF}:
        next_ch()
    match text.ch:
        case text.chEOL:
            next_ch()
            next_lex()

        # Идентификаторы и служебные слова
        case _ if text.ch in non_digit + '\\' : # !!! _a..zA..Z \uDDDD  \UDDDDDDDD
            name = text.ch
            next_ch()
            while text.ch in non_digit + digit:  # !!!!!
                name += text.ch
                next_ch()
            lex = keywords.get(name, Lex.IDENTIFIER)

        # Операции и разделители
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
        case '#': # #
            next_ch()
            if text.ch == '#': # ##
                next_ch()
                lex = Lex.DOUBLEGRID
            else:
                next_ch()
                lex = Lex.GRID
        case '(':
            next_ch()
            lex = Lex.LPAR
        case ')':
            next_ch()
            lex = Lex.RPAR
        case ';':
            next_ch()
            lex = Lex.SEMI
        case ':':
            next_ch()
            if text.ch == '>':  # :>
                next_ch()
                lex = Lex.GTCOLON
            elif text.ch == ':':
                next_ch()
                lex = Lex.DOUBLECOLON  # ::
            else:
                lex = Lex.COLON
        case ',':
            next_ch()
            lex = Lex.COMMA #,
        case '.':
            next_ch()
            if text.ch == '.':
                next_ch()
                if text.ch == '.':
                    next_ch()
                    lex = Lex.THREEDOT # ...
                else:
                    error.lexError('Должно быть три точки')
                # lex = Lex.FLOATLIT
            elif text.ch == '*':
                next_lex()
                lex = Lex.DOTMUL # .*
            else:
                lex = Lex.DOT
        case '?':
            next_ch()
            lex = Lex.QUESTIONSIGN  # ?
        case '+':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.PLUSEQ # +=
            elif text.ch == '+':
                next_ch()
                lex = Lex.INC # ++
            else:
                lex = Lex.PLUS
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
                if text.ch == '*':
                    next_ch()
                    lex = Lex.ARROWMUL
                else:
                    lex = Lex.ARROW
            else:
                lex = Lex.MINUS
        case '*':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.MULEQ
            else:
                lex = Lex.MUL
        case '/':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.DIVEQ  # /=
            elif text.ch == '/':
                end_of_the_line_comment()  # EndOfTheLineComment
                next_lex()
            elif text.ch == '*':
                traditional_comment()  # TraditionalComment
                next_lex()
            else:
                lex = Lex.DIV # /
        case '%':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.MODEQ
            elif text.ch == '>':  # %>
                next_ch()
                lex = Lex.GTMOD
            elif text.ch == ':':
                next_ch()
                if text.ch == '%':
                    next_ch()
                    if text.ch == ':':
                        next_ch()
                        lex = Lex.DOUBLEMODCOLON  # %:%:
                else:
                    lex = Lex.MODCOLON  # %:
            else:
                lex = Lex.MOD
        case '^':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.CARETEQ
            else:
                lex = Lex.CARET
        case '&':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.ANDEQ # &=
            elif text.ch == '&':
                next_ch()
                lex = Lex.ANDAND # &&
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
        case '~':
            next_ch()
            lex = Lex.TILDA
        case '!':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.NOTEQ
            else:
                lex = Lex.NOT
        case '=':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.EQEQ  # ==
            else:
                lex = Lex.EQ
        case '<':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.LTEQ  # <=
            elif text.ch == '<':
                next_ch()
                if text.ch == '=':
                    next_ch()
                    lex = Lex.LTLTEQ  # <<=
                else:  # <<
                    lex = Lex.LTLT  # <<
            elif text.ch == ':':
                next_ch()
                lex = Lex.LTCOLON  # <:
            elif text.ch == '%':
                next_ch()
                lex = Lex.LTMOD  # <%
            else:
                lex = Lex.LT  # <
        case '>':
            next_ch()
            if text.ch == '=':
                next_ch()
                lex = Lex.GTEQ # >=
            elif text.ch == '>':
                next_ch()
                if text.ch == '=':
                    next_ch()
                    lex = Lex.GTGTEQ # >>=
                else:  # >>
                    lex = Lex.GTGT # >>
            else:
                lex = Lex.GT # >

        #Литералы
        case _ if text.ch in digit:
            # if text.ch == '0':
            #     next_ch()
            #     if text.ch in 'xX':
            #         next_ch()
            #         if text.ch in hexadecimal_digits:
            #             next_ch()
            #         else:
            #             error.lexError('Ожидается шестнадцатеричная цифра')
            #         while text.ch in hexadecimal_digits:
            #             next_ch()
            #     elif text.ch in octal_digits:
            #         next_ch()
            #         while text.ch in octal_digits:
            #             next_ch()
            #         if text.ch in '89':
            #             next_ch()
            #             while text.ch in digits:
            #                 next_ch()
            #             if text.ch not in '.eEfFdD':
            #                 error.lexError('Ожидается \'.\', экспонента или суффикс типа')

            # INTEGERLIT
            if text.ch in nonzero_digit: # decimal-literal + integer_suffix
                next_ch()
                if text.ch in digit:
                    while text.ch in digit:
                        next_ch()
                    if text.ch in integer_suffix:
                        while text.ch in integer_suffix:
                            next_ch()
                            lex = Lex.INTEGERLIT
                    else:
                        lex = Lex.INTEGERLIT

            elif text.ch == '0': # octal & hex literal + integer_suffix
                next_ch()
                if text.ch in 'xX':
                    if text.ch in hexadecimal_digit:
                        while text.ch in hexadecimal_digit:
                            next_ch()
                        if text.ch in integer_suffix:
                            while text.ch in integer_suffix:
                                next_ch()
                                lex = Lex.INTEGERLIT
                        else:
                            lex = Lex.INTEGERLIT
                    else:
                        error.lexError('Ожидается шестнадцатеричная цифра')

                elif text.ch in octal_digit:
                    while text.ch in octal_digit:
                        next_ch()
                    if text.ch in integer_suffix:
                        while text.ch in integer_suffix:
                            next_ch()
                            lex = Lex.INTEGERLIT
                    else:
                        next_ch()
                        lex = Lex.INTEGERLIT
                else:
                    next_ch()
                    lex = Lex.INTEGERLIT

            # FLOATLIT
            elif text.ch in digit:
                next_ch()
                if text.ch in digit:
                    while text.ch in digit:
                        next_ch()
                    if text.ch == '.':
                        next_ch()
                        if text.ch in digit:
                            while text.ch in digit:
                                next_ch()
                                lex = Lex.FLOATLIT
                elif text.ch == '.':
                        next_ch()
                        if text.ch in digit:
                            while text.ch in digit:
                                next_ch()
                                lex = Lex.FLOATLIT
                if text.ch in exponent_part:
                    next_ch()
                    if text.ch in sign:
                        next_ch()
                        if text.ch in digit:
                            while text.ch in digit:
                                next_ch()
                                lex = Lex.FLOATLIT
                    else:
                        next_ch()
                        lex = Lex.FLOATLIT
                else:
                    lex = Lex.FLOATLIT




        # case '\'':
        #     # CHARACTER - его нужно доделать
        #     if text.ch == 'L':
        #         next_ch()
        #         if text.ch == '\'':
        #             if text.ch == '\'':
        #                 error.lexError('Ошибка в написании литерала char')



        case text.chEOT:
            lex = Lex.EOT
        case _:
            error.lexError("Недопустимый символ")