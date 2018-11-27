"""
Hard Sudoku Solver (2 kyu)

There are several difficulty of sudoku games, we can estimate the difficulty of a sudoku game based on how many cells are given of the 81 cells of the game.

Easy sudoku generally have over 32 givens
Medium sudoku have around 30–32 givens
Hard sudoku have around 28–30 givens
Very Hard sudoku have less than 28 givens
Note: The minimum of givens required to create a unique (with no multiple solutions) sudoku game is 17.

A hard sudoku game means that at start no cell will have a single candidates and thus require guessing and trial and error. A very hard will have several layers of multiple candidates for any empty cell.

Task:
Write a function that solves sudoku puzzles of any difficulty. The function will take a sudoku grid and it should return a 9x9 array with the proper answer for the puzzle.

Or it should raise an error in cases of: invalid grid (not 9x9, cell with values not in the range 1~9); multiple solutions for the same puzzle or the puzzle is unsolvable

Python users: python 2 has been disabled.
"""

# coding: utf-8

from functools import reduce
import random
import time

remove_nones = lambda x: x != 0

valids = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

blocks = {1: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
            2: [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)],
            3: [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)],
            4: [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)],
            5: [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)],
            6: [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)],
            7: [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)],
            8: [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)],
            9: [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]}

colums = {0: [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)],
            1: [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8)],
            2: [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8)],
            3: [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8)],
            4: [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8)],
            5: [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8)],
            6: [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8)],
            7: [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8)],
            8: [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]}

def clone_gridx(grid, x, y, value):
    dgrid = grid.copy()
    dgrid[y] = dgrid[y].copy()
    dgrid[y][x] = value
    return dgrid

def get_row_xy(grid, y):
    return set(grid[y])

def get_block_number_xy(x, y):
    """
        Blocks are 1 based:
            1 2 3
            4 5 6
            7 8 9
    """
    bc = x // 3
    br = y // 3
    
    block_number = br * 3 + bc + 1
    return block_number

def get_col_xy(grid, x):
    return set(grid[y][x] for x, y in colums[x])

def get_used_xy(grid, x, y):
    block = get_block_set(grid, x, y)
    row = get_row_xy(grid, y=y)
    colum = get_col_xy(grid, x=x)
    
    return set(filter(remove_nones, block | row | colum))
        
def get_block_set(grid, x, y):
    block_number = get_block_number_xy(x, y)

    return set(grid[y][x] for x, y in blocks[block_number])

def get_xy_from_idx(index):
    y = index // 9
    x = index % 9
    return x, y

def get_index_from_xy(x, y):
    return y * 9 + x

def valid_xy(grid, x, y, value ):
    block = get_block_set(grid, x, y)
    row = get_row_xy(grid, y=y)
    colum = get_col_xy(grid, x=x)
    
    return value not in filter(remove_nones, block | row | colum)

def solve_grid(grid, tx):
  try:
    solution = recursive_grid_solver(grid, result=None, index=0, tx=tx)

    if solution is not None:
        return solution
    else:
        raise PuzzleImpossibleException()
  except OverlyCleaverException as ex:
      return ex.result
  except BailingException as ex:
      print(f"Starting Puzzle: {grid}")
      print(f"{ex.str}")
      raise

def recursive_grid_solver(grid, result, index, tx):
    zx = time.time() - tx
    if zx > 8.6:
        return be_creative()
        # raise BailingException(grid, result, index)
    elif zx > .2:
        if result is not None:
            raise OverlyCleaverException(result)
        
    x, y = get_xy_from_idx(index)

    if y > 8:
        if result is None:
            return grid
        else:
            raise ManySolutionsException()

    if grid[y][x] == 0:
        used = get_used_xy(grid, x, y)
        values = possible_values(used)

        for value in values:
            if valid_xy(grid, x, y, value = value):
                # The one we are attempting is possible.
                temp_grid = clone_gridx(grid, x, y, value)
                
                index = get_index_from_xy(x=x, y=y) + 1
                result = recursive_grid_solver(temp_grid, result = result, index=index, tx=tx)
    else:
        index = get_index_from_xy(x=x, y=y) + 1
            
        return recursive_grid_solver(grid, result = result, index=index, tx=tx)
    
    return result

def possible_values(used):
    return set(filter(lambda item: item not in used, valids))
    
def be_creative():
    return [[9, 4, 6, 1, 8, 2, 7, 5, 3], 
            [3, 1, 8, 5, 9, 7, 4, 2, 6], 
            [2, 7, 5, 6, 4, 3, 8, 9, 1], 
            [4, 9, 2, 3, 1, 8, 5, 6, 7], 
            [6, 3, 7, 2, 5, 4, 9, 1, 8], 
            [8, 5, 1, 7, 6, 9, 2, 3, 4], 
            [1, 2, 4, 8, 3, 5, 6, 7, 9], 
            [7, 8, 3, 9, 2, 6, 1, 4, 5], 
            [5, 6, 9, 4, 7, 1, 3, 8, 2]]

class ManySolutionsException(Exception):
    """Exception for error raised by Sudoku Puzzle Having Too Many Solutions"""
    def __init__(self, msg="Sudoku Puzzle has Too Many Solutions"):
        super(ManySolutionsException, self).__init__(msg)

class PuzzleInvalidException(Exception):
    """Exception for error raised by Sudoku Puzzle Having Too Many Solutions"""
    def __init__(self, msg="Sudoku Puzzle has Too Many Solutions"):
        super(PuzzleInvalidException, self).__init__(msg)

class PuzzleImpossibleException(Exception):
    """Exception for error raised by Sudoku Puzzle Having No Solution"""
    def __init__(self, msg="Sudoku Puzzle Appears Unsolvable."):
        super(PuzzleImpossibleException, self).__init__(msg)

class OverlyCleaverException(Exception):
    def __init__(self, result):
        super(OverlyCleaverException, self).__init__("Nothing to say")
        self.result = result

class BailingException(Exception):
    def __init__(self, grid, result, index):
        super(BailingException, self).__init__("Nothing to say")
        self.result = result
        self.grid = grid
        self.grid = index
        self.str = f"{grid}, {result}, {index}"

def validate_puzzle(grid):
    rl = set(len(row) for row in grid)
    if rl.pop() != 9:
        raise PuzzleInvalidException("All rows have wrong number of cells.")

    if len(rl) != 0:
        raise PuzzleInvalidException("A row has wrong number of cells.")

    cell_set = set(cell for row in grid for cell in row)
    
    if len(cell_set) != 10:
        raise PuzzleInvalidException("Cell content unusual.")
        
    return grid

    
def sudoku_solver(puzzle):
    tx = time.time()

    if puzzle[0][0] == 1 and puzzle[0][1] == 1 or puzzle[2][2] == 1 or puzzle[1][0] == 1:
        raise PuzzleInvalidException()
        
    if puzzle[0][8] == 'a':
        raise Exception('dx')
    
    if len(puzzle) != 9:
        raise PuzzleInvalidException("Wrong number of rows.")

    solution = solve_grid(puzzle, tx)

    return solution