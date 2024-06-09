#Синтаксический анализатор

import text
import scan


def testText():
    text.next_ch()
    while text.ch != text.chEOT:
        text.next_ch()


def Compile():
    n = 0
    while text.i < len(text.src):
        text.next_ch()
        scan.next_lex()
        while scan.lex != scan.Lex.EOT:
            n += 1
            scan.lex_dict[scan.lex.name] += 1
            scan.next_lex()
            # print(n, scan.lex)
    print("\nЧисло лексем:", n)
    for key in scan.lex_dict:
        if scan.lex_dict[key] != 0:
            print("{:20}{:6}{:8.2f}".format(key, scan.lex_dict[key], scan.lex_dict[key] * 100 / n) + '%')
