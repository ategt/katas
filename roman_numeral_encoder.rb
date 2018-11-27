# Roman Numerals Encoder (6 kyu)

# Create a function taking a positive integer as its parameter and returning a string containing the Roman Numeral representation of that integer.

# Modern Roman numerals are written by expressing each digit separately starting with the left most digit and skipping any digit with a value of zero. In Roman numerals 1990 is rendered: 1000=M, 900=CM, 90=XC; resulting in MCMXC. 2008 is written as 2000=MM, 8=VIII; or MMVIII. 1666 uses each Roman symbol in descending order: MDCLXVI.

# Example:

# solution(1000) # should return 'M'
# Help:

# Symbol    Value
# I          1
# V          5
# X          10
# L          50
# C          100
# D          500
# M          1,000
# Remember that there can't be more than 3 identical symbols in a row.

# More about roman numerals - http://en.wikipedia.org/wiki/Roman_numerals


@roman_symbols = ['I', 'V', 'X', 'L', 'C', 'D', 'M', 'MMMMM', 'MMMMMMMMMM']  # I know the last two are wrong, but I liked placeholders better than a custom if.

def solution(number)
  accumulator =
    number.to_s.reverse.each_char.with_index.map do |letter, index|
      character_map(letter.to_i, *@roman_symbols[index * 2, 3])
    end
  accumulator.reverse.join  
end

def character_map(input_int, single, half, higher_single)
  if input_int <= 3
    single * input_int
  elsif input_int == 4
    single + half
  elsif input_int >= 5 and input_int <= 8
    half + single * (input_int - 5)
  elsif input_int == 9
    single + higher_single
  else
    raise
  end
end
