/*
Permutations (4 kyu)

In this kata you have to create all permutations of an input string and remove duplicates, if present. This means, you have to shuffle all letters from the input in all possible orders.

Examples:

permutations('a'); # ['a']
permutations('ab'); # ['ab', 'ba']
permutations('aabb'); # ['aabb', 'abab', 'abba', 'baab', 'baba', 'bbaa']
The order of the permutations doesn't matter.

*/

// Flatten function came from stack overflow.
// I lost the url for the specific page.
function flatten(input) {
  const stack = [...input];
  const res = [];
  while (stack.length) {
    // pop value from stack
    const next = stack.pop();
    if (Array.isArray(next)) {
      // push back array items, won't modify the original input
      stack.push(...next);
    } else {
      res.push(next);
    }
  }
  //reverse to restore input order
  return res.reverse();
}

function permutations(head, tail='', depth=0){
  var letters = head.split('').length
  if(letters < 1){
    return tail
  } else {
    return [...new Set(flatten(head.split('').map(function(item, index){
      var alist = permutations(head.substr(0, index) + head.substr(index+1), tail+head[index], depth+1)
      return alist
    })))]
  }
}
