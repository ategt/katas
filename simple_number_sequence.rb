# Simple number sequence (5 kyu)

# In this Kata, you will be given a string of numbers in sequence and your task will be to return the missing number. If there is no number missing or there is an error in the sequence, return -1.

# For example:

# missing("123567") = 4 
# missing("899091939495") = 92
# missing("9899101102") = 100
# missing("599600601602") = -1 -- no number missing
# missing("8990919395") = -1 -- error in sequence. Both 92 and 94 missing.
# The sequence will always be in ascending order.

# More examples in the test cases.

# Good luck!

def missing s
  maximum_number_length = s.length / 3
  options =
    (1..maximum_number_length).
                            to_a.
                            select { |starting_digits| test_plaussibility(starting_digits, s) } .
                            map { |starting_digit_count| find_missing(starting_digit_count, s) } .
                            select { |nillables| !nillables.nil? }
                            
  return options.last if options.one?
  -1
end

def test_plaussibility digit_count, s
  test_integer = s[0, digit_count].to_i
  s =~ /\A(#{test_integer}#{test_integer+1}|#{test_integer}#{test_integer+2}#{test_integer+3}).*/
end

def find_missing starting_digit_count, s
  missings = []
  current_int = s[0, starting_digit_count].to_i
  test_s = current_int.to_s
  while test_s.length < s.length
    current_int += 1
    test_s += current_int.to_s
    if !s.start_with? test_s
      missings << current_int
      break if missings.size > 1
      test_s = test_s.sub(current_int.to_s,'')
    end
  end
  missings.last if missings.one?
end
