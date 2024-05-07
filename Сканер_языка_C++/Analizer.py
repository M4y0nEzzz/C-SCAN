#Реализация задания варианта - подсчет общего числа лексем и
#подсчет частоты (абсолютной и относительной) лексем каждого класса.
import Text
import Scan
def testText():
    Text.next_ch()
    while Text.ch != Text.chEOT:
        Text.next_ch()

def Compile():
    Text.next_ch()
    lex = Scan.next_lex()
    n = 0
    while lex != Scan.Lex.EOT:
        n += 1
        Scan.lex_dict[lex.name] += 1
        lex = Scan.next_lex()
        # print(n, lex)
    print("\nЧисло лексем:", n)
    for key in Scan.lex_dict:
        if Scan.lex_dict[key] != 0:
            print("{:20}{:6}{:8.2f}".format(key, Scan.lex_dict[key], Scan.lex_dict[key] * 100 / n) + '%')