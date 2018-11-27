# Permutations (4 kyu)

# In this kata you have to create all permutations of an input string and remove duplicates, if present. This means, you have to shuffle all letters from the input in all possible orders.

# Examples:

# permutations('a'); # ['a']
# permutations('ab'); # ['ab', 'ba']
# permutations('aabb'); # ['aabb', 'abab', 'abba', 'baab', 'baba', 'bbaa']
# The order of the permutations doesn't matter.

def permutations(head, tail='', depth=0)
  letters = head.split('').length
  if letters < 1
    tail
  else
    (0...letters).map do |iteration|
      temp_string = head.dup
      swap_char = temp_string.slice! iteration
      permutations(temp_string, "#{tail}#{swap_char}", depth+1)
    end.flatten.uniq
  end
end
