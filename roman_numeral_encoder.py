"""
Roman Numerals Encoder (6 kyu)

Create a function taking a positive integer as its parameter and returning a string containing the Roman Numeral representation of that integer.

Modern Roman numerals are written by expressing each digit separately starting with the left most digit and skipping any digit with a value of zero. In Roman numerals 1990 is rendered: 1000=M, 900=CM, 90=XC; resulting in MCMXC. 2008 is written as 2000=MM, 8=VIII; or MMVIII. 1666 uses each Roman symbol in descending order: MDCLXVI.

Example:

solution(1000) # should return 'M'
Help:

Symbol    Value
I          1
V          5
X          10
L          50
C          100
D          500
M          1,000
Remember that there can't be more than 3 identical symbols in a row.

More about roman numerals - http://en.wikipedia.org/wiki/Roman_numerals

"""

def romanize(input):
    accumulator = []
    reversed_string = str(input)[::-1]
    for index, letter in  enumerate(reversed_string):
        int_letter = int(letter)
        if index == 0:
            accumulator.append( characterMap(int_letter, 'I', 'V', 'X') )
        elif index == 1:
            accumulator.append( characterMap(int_letter, 'X', 'L', 'C') )
        elif index == 2:
            accumulator.append( characterMap(int_letter, 'C', 'D', 'M') )
        elif index == 3:
            accumulator.append( characterMap(int_letter, 'M', 'D', 'M') )
    return "".join(list(reversed(accumulator)))
    
def characterMap(fint, single, half, higher_single):
    if fint <= 3:
        return single * fint
    elif fint == 4:
        return single + half
    elif fint >= 5 and fint <= 8:
        return half + single * (fint - 5)
    elif fint == 9:
        return single + higher_single
        
def solution(n):
    return romanize(n)
          
roman_numeral_symbols = 'IVXLCDM'

def solution(input):
    accumulator = []
    reversed_string = reversed(str(input))
    for index, letter in  enumerate(reversed_string):
        accumulator.append( characterMap(int(letter), *roman_numeral_symbols[index * 2 : index * 2 + 3]))
    return "".join(list(reversed(accumulator)))
    
def characterMap(fint, single, half = None, higher_single = None):
    if fint <= 3:
        return single * fint
    elif fint == 4:
        return single + half
    elif fint >= 5 and fint <= 8:
        return half + single * (fint - 5)
    elif fint == 9:
        return single + higher_single
