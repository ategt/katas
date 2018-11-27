"""
Sudoku Solution Validator (4 kyu)

Sudoku Background
Sudoku is a game played on a 9x9 grid. The goal of the game is to fill all cells of the grid with digits from 1 to 9, so that each column, each row, and each of the nine 3x3 sub-grids (also known as blocks) contain all of the digits from 1 to 9. 
(More info at: http://en.wikipedia.org/wiki/Sudoku)

Sudoku Solution Validator
Write a function validSolution/ValidateSolution/valid_solution() that accepts a 2D array representing a Sudoku board, and returns true if it is a valid solution, or false otherwise. The cells of the sudoku board may also contain 0's, which will represent empty cells. Boards containing one or more zeroes are considered to be invalid solutions.

The board is always 9 cells by 9 cells, and every cell only contains integers from 0 to 9.

Examples
validSolution([
  [5, 3, 4, 6, 7, 8, 9, 1, 2],
  [6, 7, 2, 1, 9, 5, 3, 4, 8],
  [1, 9, 8, 3, 4, 2, 5, 6, 7],
  [8, 5, 9, 7, 6, 1, 4, 2, 3],
  [4, 2, 6, 8, 5, 3, 7, 9, 1],
  [7, 1, 3, 9, 2, 4, 8, 5, 6],
  [9, 6, 1, 5, 3, 7, 2, 8, 4],
  [2, 8, 7, 4, 1, 9, 6, 3, 5],
  [3, 4, 5, 2, 8, 6, 1, 7, 9]
]); // => true
validSolution([
  [5, 3, 4, 6, 7, 8, 9, 1, 2], 
  [6, 7, 2, 1, 9, 0, 3, 4, 8],
  [1, 0, 0, 3, 4, 2, 5, 6, 0],
  [8, 5, 9, 7, 6, 1, 0, 2, 0],
  [4, 2, 6, 8, 5, 3, 7, 9, 1],
  [7, 1, 3, 9, 2, 4, 8, 5, 6],
  [9, 0, 1, 5, 3, 7, 2, 1, 4],
  [2, 8, 7, 4, 1, 9, 6, 3, 5],
  [3, 0, 0, 4, 8, 1, 1, 7, 9]
]); // => false

"""

from functools import reduce
import random

blank_row = lambda: [None] * 9
blank_grid = lambda: [blank_row() for _ in range(9)]
valid_numbers = lambda: reduce(lambda acc, item: [*acc, item], range(1,10), [])
remove_nones = lambda x: x is not None

def clone_grid(donor_grid):
    recipient_grid = blank_grid()
    for y in range(len(donor_grid)):
        for x in range(len(donor_grid[0])):
            recipient_grid[y][x] = donor_grid[y][x]

    return recipient_grid            

def set_coords(grid, col, row, value):
    grid[row][col] = value
    return grid

def get_row(grid, row_num):
    return grid[row_num-1]

def get_block_number(col_num, row_num):
    """
        Blocks are 1 based:
            1 2 3
            4 5 6
            7 8 9
    """
    bc = ( col_num - 1 ) // 3
    br = ( row_num - 1 ) // 3
    
    block_number = br * 3 + bc + 1
    return block_number

def get_col(grid, col_num):
    return [ col for row_num, row in enumerate(grid) for test_col_num, col in enumerate(row) if test_col_num + 1 == col_num ]

def random_valid_numbers():
    vns = valid_numbers()
    random.shuffle(vns)
    return vns

def get_used(grid, col_num, row_num):
    block = get_block(grid, col_num=col_num, row_num=row_num)
    row = get_row(grid, row_num=row_num)
    colum = get_col(grid, col_num=col_num)
    
    return list(filter(remove_nones, [*block, *row, *colum]))

def get_block(grid, col_num, row_num):
    block_number = get_block_number(col_num=col_num, row_num=row_num)
    return [ col for row_num, row in enumerate(grid) for col_num, col in enumerate(row) if get_block_number(col_num + 1, row_num + 1) == block_number ]
        
def get_coords_from_idx(index):
    row_num = ( index - 1 ) // 9 + 1
    col_num = ( index - 1 ) % 9 + 1
    return col_num, row_num

def get_index_from_coords(col_num, row_num):
    return ( row_num - 1 ) * 9 + col_num

def valid(grid, col_num, row_num, value = None):
    test_value = grid[row_num-1][col_num-1] if value is None else value
    
    block = get_block(grid, col_num, row_num)
    row = get_row(grid, row_num=row_num)
    colum = get_col(grid, col_num=col_num)
    
    return test_value not in block and test_value not in row and test_value not in colum

def recursive_grid_populator(grid, index = 1):
    if index > 81:
        return True, grid

    col_num, row_num = get_coords_from_idx(index)
    
    for value in random_valid_numbers():
        if valid(grid, row_num=row_num, col_num=col_num, value = value):
            # The one we are attempting is possible.
            temp_grid = clone_grid(grid)
            temp_grid[row_num-1][col_num-1] = value
            working_out, filled_in_grid = recursive_grid_populator(temp_grid, index = get_index_from_coords(row_num=row_num, col_num=col_num) + 1)
            
            if working_out:
                return working_out, filled_in_grid

    # Grid Not valid
    return False, grid

def mask_grid_to_puzzle(grid, cells=None, verbose=False, **kwargs):
    grid = clone_grid(grid)

    indexes = reduce(lambda acc, item: [*acc, item], range(1,82), [])
    random.shuffle(indexes)

    for ix, index in enumerate(indexes):
        col_num, row_num = get_coords_from_idx(index)
        temp_grid = clone_grid(grid)
        temp_grid[col_num-1][row_num-1] = None

        if verbose:
            print("Testing ", ix, " Values Given", _values_given(temp_grid))

        if is_puzzle_solution_unique(temp_grid):
            grid = temp_grid

        if cells is not None and _values_given(grid) == cells:
            return grid
        
    return grid

def solve_grid(grid):
    solutions = recursive_grid_solver(grid)

    if len(solutions) == 1:
        return solutions[0]
    else:
        raise Exception("Sudoku Puzzle Appears Unsolvable.")

def recursive_grid_solver(grid, results=[], index = 1):
    if index > 81:
        results.append(clone_grid(grid))
        if len(results) > 1:
            raise ManySolutionsException()
        return results

    col_num, row_num = get_coords_from_idx(index)
    
    values = None
    if grid[row_num-1][col_num-1] is None:
        used = get_used(grid, col_num, row_num)
        values = possible_values(used)
    else:
        values = [grid[row_num-1][col_num-1]]
    
    for value in values:
        if grid[row_num-1][col_num-1] is not None or valid(grid, row_num=row_num, col_num=col_num, value = value):
            # The one we are attempting is possible.
            temp_grid = clone_grid(grid)
            temp_grid[row_num-1][col_num-1] = value
            results = recursive_grid_solver(temp_grid, results = results, index = get_index_from_coords(row_num=row_num, col_num=col_num) + 1)

    return results

def possible_values(used):
    return list(filter(lambda item: item not in used, valid_numbers()))

def is_puzzle_solution_unique(grid):
    try:
        _solutions = recursive_grid_solver(grid, results=[])
        return True
    except ManySolutionsException:
        return False

def rate_puzzle(grid):
    starting_values_count = _values_given(grid)

    print(starting_values_count, "Starting Values")

    if starting_values_count > 23:
        return "Easy"
    elif starting_values_count > 20:
        return "Medium"
    elif starting_values_count > 17:
        return "Hard"
    else:
        return "Very Hard"

def _values_given(grid):
    flattened_grid = reduce(lambda accum, item: [*accum, *item], grid, [])
    values = list(filter(remove_nones, flattened_grid))
    starting_values_count = len(values)
    return starting_values_count

def build_sudoku(**kwargs):
    grid = blank_grid()
    _valid, result = recursive_grid_populator(grid)

    if kwargs.get('debug', False):
        import json
        print(json.dumps(result))

    puzzle = mask_grid_to_puzzle(result, **kwargs)

    print("Puzzle is ", rate_puzzle(puzzle))

    return puzzle, result

class ManySolutionsException(Exception):
    """Exception for error raised by Sudoku Puzzle Having Too Many Solutions"""
    def __init__(self, msg="Sudoku Puzzle has Too Many Solutions"):
        super(ManySolutionsException, self).__init__(msg)

def validSolution(grid):
    for index in range(1, 82):
        col_num, row_num = get_coords_from_idx(index)

        value = grid[row_num-1][col_num-1]
    
        temp_grid = clone_grid(grid)
        temp_grid[row_num-1][col_num-1] = None

        if not valid(temp_grid, row_num=row_num, col_num=col_num, value = value):
            return False

    return True
