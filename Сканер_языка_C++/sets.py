from string import digits

with open('output.txt', 'r', encoding='utf-8') as file:
    letter = file.read()
    letter = letter + '#'
letter_or_digit = letter + digits