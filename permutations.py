# Permutations (4 kyu)

# In this kata you have to create all permutations of an input string and remove duplicates, if present. This means, you have to shuffle all letters from the input in all possible orders.

# Examples:

# permutations('a'); # ['a']
# permutations('ab'); # ['ab', 'ba']
# permutations('aabb'); # ['aabb', 'abab', 'abba', 'baab', 'baba', 'bbaa']
# The order of the permutations doesn't matter.

def permutations(head, tail='', depth=0):
  letters = len(head)
  if letters < 1:
    return tail
  else:
    alist = [permutations(head[0: iteration] + head[iteration+1:], tail+head[iteration], depth+1) for iteration in range(letters)]
    return list(set(flatten(alist))) if isinstance(alist[0], list) else alist

    
def flatten(alist):
    return [item for sublist in alist for item in sublist]
