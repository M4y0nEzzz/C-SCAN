#Данный модуль - и есть сканер

import Analizer
import Text

def Init():
    Text.reset()

print("Лексический анализатор (т.н. сканер) языка С++")
Init()
Analizer.Compile()