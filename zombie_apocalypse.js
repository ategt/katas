/*
Stop the Zombie Apocalypse! (5 kyu)


You are a number. But that's good for you since you live in the beautiful world, where the only living creatures are numbers. Unfortunately, a nasty zombie virus is spreading out in the digital cities. You work at the digital CDC and your job is to look over the city maps and tell which areas are contaminated by the zombie virus so the digital army would know where to drop the bombs. They are the new kind of digital zombies which can travel only in vertical and horizontal directions and infect only numbers same as them, but don't let it fool you, they're still very dangerous. Time is running out...

You'll be given two-dimensional array with numbers in it. For some mysterious reason patient zero is always found in north west area of the city (element [0][0] of the matrix) and the plague spreads from there to other cells by moving left, right, up or down. You must create a function that returns a map (2-dimensional array) with all the contaminated areas marked as 1 and virus-free marked as 0.

In other words: find all the matrix elements with the same value as [0][0] that you can go to by moving only down, up, right or left from [0][0] - without going into a field storing any other value.

For example:

var city1 = [
    [7, 2, 3],
    [7, 2, 3],
    [1, 2, 7]
];

var contaminatedInCity1 = [
    [1, 0, 0],
    [1, 0, 0],
    [0, 0, 0]
];// number 7 is a zombie, but the 7 in bottom right corner is not a zombie yet - the virus didn't get there.

var city2 = [
    [9, 1, 2],
    [9, 9, 9],
    [7, 4, 9],
    [7, 9, 7]
]; 

var contaminatedInCity2 = [
    [1, 0, 0],
    [1, 1, 1],
    [0, 0, 1],
    [0, 0, 0]
];//infection inflicted the 9s, but the virus didn't get to the one in the south of the city yet.
*/

function process(input_matrix) {
    var result_matrix = initalize_result(input_matrix)
    var origin_number = input_matrix[0][0]

    var old_result_count = -1
    var new_result_count = 0

    while(old_result_count < new_result_count){
      var temp_result_matrix = result_matrix.map(function(row, y){ 
        return row.map(function(item, x){
          if( detect( x, y, input_matrix, result_matrix, origin_number )){
            return 1
          } else {
            return 0
          }
        })
      })

      old_result_count = flatten(result_matrix).filter(function(item) { return item == 1 }).length
      result_matrix = merge_matrices(result_matrix, temp_result_matrix)
      new_result_count = flatten(result_matrix).filter(function(item) { return item == 1 }).length
    }

    return result_matrix
}

function initalize_result(input_matrix) {
  var result = input_matrix.map(function(y){ return y.map(function(x){ return 0 }) })
  result[0][0] = 1
  return result
}

function merge_matrices(source, additional){
  return source.map(function(row, y){
    return row.map(function(item, x) {
      if(item == 1 || additional[y][x] == 1){
        return 1
      } else {
        return 0
      }
    })
  })
}

function detect(x, y, input_matrix, result_matrix, origin_number){
  if(input_matrix[y][x] == origin_number){
    if(x - 1 >= 0 && result_matrix[y][x-1] == 1){
      return true
    } else if( x + 1 < input_matrix[y].length && result_matrix[y][x + 1] == 1) {
      return true
    } else if (y - 1 >= 0 && result_matrix[y-1][x] == 1) {
      return true
    } else if (y + 1 < input_matrix.length && result_matrix[y+1][x] == 1) {
      return true
    } else {
      return false
    }  
  } else {
    return false
  }
}

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

function findZombies(matrix) {
  return process(matrix)
}