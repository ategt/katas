"""
4 By 4 Skyscrapers (4 kyu)

In a grid of 4 by 4 squares you want to place a skyscraper in each square with only some clues:

The height of the skyscrapers is between 1 and 4
No two skyscrapers in a row or column may have the same number of floors
A clue is the number of skyscrapers that you can see in a row or column from the outside
Higher skyscrapers block the view of lower skyscrapers located behind them

Can you write a program that can solve this puzzle? 

Example: 

To understand how the puzzle works, this is an example of a row with 2 clues. Seen from the left side there are 4 buildings visible while seen from the right side only 1: 

 4                                   1

There is only one way in which the skyscrapers can be placed. From left-to-right all four buildings must be visible and no building may hide behind another building: 

 4   1   2   3   4   1

Example of a 4 by 4 puzzle with the solution: 

                     1   2    
                      
                     2
 1                    
                      
             3        

             1   2    
     2   1   4   3    
     3   4   1   2   2
 1   4   2   3   1    
     1   3   2   4    
             3        

Task: 

Finish:
function solvePuzzle(clues)
Pass the clues in an array of 16 items. This array contains the clues around the clock, index: 
     0   1     2       3      
 15                  4
 14                  5
 13                  6
 12                  7
    11  10   9   8    
If no clue is available, add value 0
Each puzzle has only one possible solution
SolvePuzzle() returns matrix int[][]. The first indexer is for the row, the second indexer for the column. (Python: returns 4-tuple of 4-tuples, Ruby: 4-Array of 4-Arrays)
If you finished this kata you can use your solution as a base for the more challenging kata: 6 By 6 Skyscrapers
"""

def setup_visual_possibilities():
    return [(4, 1, (1, 2, 3, 4)),
             (3, 2, (1, 2, 4, 3)),
             (3, 1, (1, 3, 2, 4)),
             (3, 2, (1, 3, 4, 2)),
             (2, 2, (1, 4, 2, 3)),
             (2, 3, (1, 4, 3, 2)),
             (3, 1, (2, 1, 3, 4)),
             (2, 2, (2, 1, 4, 3)),
             (3, 1, (2, 3, 1, 4)),
             (3, 2, (2, 3, 4, 1)),
             (2, 2, (2, 4, 1, 3)),
             (2, 3, (2, 4, 3, 1)),
             (2, 1, (3, 1, 2, 4)),
             (2, 2, (3, 1, 4, 2)),
             (2, 1, (3, 2, 1, 4)),
             (2, 2, (3, 2, 4, 1)),
             (2, 2, (3, 4, 1, 2)),
             (2, 3, (3, 4, 2, 1)),
             (1, 2, (4, 1, 2, 3)),
             (1, 3, (4, 1, 3, 2)),
             (1, 2, (4, 2, 1, 3)),
             (1, 3, (4, 2, 3, 1)),
             (1, 3, (4, 3, 1, 2)),
             (1, 4, (4, 3, 2, 1)),
             (0, 1, (1, 2, 3, 4)),
             (0, 2, (1, 2, 4, 3)),
             (0, 1, (1, 3, 2, 4)),
             (0, 2, (1, 3, 4, 2)),
             (0, 2, (1, 4, 2, 3)),
             (0, 3, (1, 4, 3, 2)),
             (0, 1, (2, 1, 3, 4)),
             (0, 2, (2, 1, 4, 3)),
             (0, 1, (2, 3, 1, 4)),
             (0, 2, (2, 3, 4, 1)),
             (0, 2, (2, 4, 1, 3)),
             (0, 3, (2, 4, 3, 1)),
             (0, 1, (3, 1, 2, 4)),
             (0, 2, (3, 1, 4, 2)),
             (0, 1, (3, 2, 1, 4)),
             (0, 2, (3, 2, 4, 1)),
             (0, 2, (3, 4, 1, 2)),
             (0, 3, (3, 4, 2, 1)),
             (0, 2, (4, 1, 2, 3)),
             (0, 3, (4, 1, 3, 2)),
             (0, 2, (4, 2, 1, 3)),
             (0, 3, (4, 2, 3, 1)),
             (0, 3, (4, 3, 1, 2)),
             (0, 4, (4, 3, 2, 1)),
             (4, 0, (1, 2, 3, 4)),
             (3, 0, (1, 2, 4, 3)),
             (3, 0, (1, 3, 2, 4)),
             (3, 0, (1, 3, 4, 2)),
             (2, 0, (1, 4, 2, 3)),
             (2, 0, (1, 4, 3, 2)),
             (3, 0, (2, 1, 3, 4)),
             (2, 0, (2, 1, 4, 3)),
             (3, 0, (2, 3, 1, 4)),
             (3, 0, (2, 3, 4, 1)),
             (2, 0, (2, 4, 1, 3)),
             (2, 0, (2, 4, 3, 1)),
             (2, 0, (3, 1, 2, 4)),
             (2, 0, (3, 1, 4, 2)),
             (2, 0, (3, 2, 1, 4)),
             (2, 0, (3, 2, 4, 1)),
             (2, 0, (3, 4, 1, 2)),
             (2, 0, (3, 4, 2, 1)),
             (1, 0, (4, 1, 2, 3)),
             (1, 0, (4, 1, 3, 2)),
             (1, 0, (4, 2, 1, 3)),
             (1, 0, (4, 2, 3, 1)),
             (1, 0, (4, 3, 1, 2)),
             (1, 0, (4, 3, 2, 1)),
             (0, 0, (1, 2, 3, 4)),
             (0, 0, (1, 2, 4, 3)),
             (0, 0, (1, 3, 2, 4)),
             (0, 0, (1, 3, 4, 2)),
             (0, 0, (1, 4, 2, 3)),
             (0, 0, (1, 4, 3, 2)),
             (0, 0, (2, 1, 3, 4)),
             (0, 0, (2, 1, 4, 3)),
             (0, 0, (2, 3, 1, 4)),
             (0, 0, (2, 3, 4, 1)),
             (0, 0, (2, 4, 1, 3)),
             (0, 0, (2, 4, 3, 1)),
             (0, 0, (3, 1, 2, 4)),
             (0, 0, (3, 1, 4, 2)),
             (0, 0, (3, 2, 1, 4)),
             (0, 0, (3, 2, 4, 1)),
             (0, 0, (3, 4, 1, 2)),
             (0, 0, (3, 4, 2, 1)),
             (0, 0, (4, 1, 2, 3)),
             (0, 0, (4, 1, 3, 2)),
             (0, 0, (4, 2, 1, 3)),
             (0, 0, (4, 2, 3, 1)),
             (0, 0, (4, 3, 1, 2)),
             (0, 0, (4, 3, 2, 1))]

def visible(tower_list):
    current_tallest_height = 0
    tower_visible_count = 0
    
    for tower_height in tower_list:
        if tower_height > current_tallest_height:
            tower_visible_count += 1
            current_tallest_height = tower_height

    return tower_visible_count

def breakup_clues(clues, side_length):
    top = clues[0:side_length]
    right = clues[side_length:side_length*2]
    bottom = clues[side_length*2:side_length*3]
    left = clues[side_length*3:side_length*4]
    
    return top, right, bottom, left

def line_valid(line):
    return len(set(line)) == 4

def build_rows(y, current_possibles):
    return list(map(lambda item: item, filter(lambda item: item is not None and len(item) == 4, _build_rows(x=0, y=y, current_possibles = current_possibles))))

def build_colums(x, current_possibles):
    return list(map(lambda item: item, filter(lambda item: item is not None and len(item) == 4, _build_colum(x=x, y=0, current_possibles = current_possibles))))

def _build_colum(x, y, current_possibles):
    possible_values = current_possibles.get((x, y), [])

    results = [None]

    for value in possible_values:
        for remainder in _build_colum(x=x, y=y+1, current_possibles=current_possibles):
            result = [value]
            if remainder is not None:
                result.extend(remainder)

            results.append(result)

    return results

def _build_rows(x, y, current_possibles):
    possible_values = current_possibles.get((x, y), [])

    results = [None]

    for value in possible_values:
        for remainder in _build_rows(x=x+1, y=y, current_possibles=current_possibles):
            result = [value]
            if remainder is not None:
                result.extend(remainder)

            results.append(result)

    return results

def validate_row(y, current_possibles, left_and_right):
    possible_row_permutations = build_rows(y=y, current_possibles = current_possibles)
    l, r = left_and_right[y]
    return [row_canidate for row_canidate in possible_row_permutations if line_with_bounds_possible(row_canidate, l, r)]

def validate_column(x, current_possibles, top_and_bottom):
    possible_column_permutations = build_colums(x=x, current_possibles = current_possibles)
    t, b = top_and_bottom[x]
    return [column_canidate for column_canidate in possible_column_permutations if line_with_bounds_possible(column_canidate, t, b)]

def build_dict_from_possible_rows_and_columns(possible_rows, possible_columns, cells):
    "dict_of_possible_values"
    return dict(((x,y), {possible_colum[y] for possible_colum in possible_columns[x]} & {possible_row[x] for possible_row in possible_rows[y]}) for x, y in cells)

def render_dict_to_answer(answer_dict):
    return tuple(tuple(answer_dict[(x, y)].pop() for x in range(0, 4)) for y in range(0, 4))

def check_for_answer(answer_dict):
    return len({len(answer_dict[(x, y)]) for x in range(0, 4) for y in range(0, 4)}) == 1

def possible_lines(towers_visible, opposite_side_towers_visible, vis_pos_list):
        return list(map(lambda tpl: tpl[2], filter(lambda tpl: tpl[0] == towers_visible and tpl[1] == opposite_side_towers_visible, vis_pos_list)))

def line_with_bounds_possible(line, l, r):
    return ( l == 0 or visible(line) == l ) and ( r == 0 or visible(reversed(line)) == r )

def validate_columns(possible_x_columns):
    return [tuple(filter(line_valid, column_candidates)) for column_candidates in possible_x_columns]

def validate_rows(possible_x_rows):
    return [tuple(filter(line_valid, row_candidates)) for row_candidates in possible_x_rows]

def split_dictionary_into_rows_and_columns(dict_of_possible_values):
    possible_x_columns = [build_colums(i, dict_of_possible_values) for i in range(4)]
    possible_x_rows    = [build_rows(i, dict_of_possible_values) for i in range(4)]

    return validate_lines(possible_x_rows), validate_lines(possible_x_columns)

def validate_side_of_lines(side_of_line_candidates_collection):
    return [validate_lines(line_candidates_collection) for line_candidates_collection in side_of_line_candidates_collection]

def validate_lines(line_candidates_collection):
    return [tuple(filter(line_valid, line_candidates)) for line_candidates in line_candidates_collection]

def solve(clues):
    vis_pos_list = setup_visual_possibilities()
    top, right, bottom, left = breakup_clues(clues, 4)

    right, corrected_left = right, list(reversed(left))
    left_and_right = list(zip(corrected_left, right))

    top, corrected_bottom = top, list(reversed(bottom))
    top_and_bottom = list(zip(top,corrected_bottom))

    cells = {(x, y) for y in range(0, 4) for x in range(0, 4)}

    possible_rows = [possible_lines(x, y, vis_pos_list) for x,y in left_and_right]
    possible_columns = [possible_lines(x, y, vis_pos_list) for x,y in top_and_bottom]

    dict_of_possible_values = build_dict_from_possible_rows_and_columns(possible_rows, possible_columns, cells)

    validated_rows, validated_columns = split_dictionary_into_rows_and_columns(dict_of_possible_values)

    revised_dict_of_possible_values = build_dict_from_possible_rows_and_columns(validated_rows, validated_columns, cells)

    for _ in range(50):
        revalidated_rows, revalidated_columns = split_dictionary_into_rows_and_columns(revised_dict_of_possible_values)

        revalidated_rows = [[row_canidate for row_canidate in possible_row_permutations if line_with_bounds_possible(row_canidate, l, r)] for possible_row_permutations, l, r in zip(revalidated_rows, corrected_left, right )]
        revalidated_columns = [[column_canidate for column_canidate in possible_column_permutations if line_with_bounds_possible(column_canidate, t, b)] for possible_column_permutations, t, b in zip(revalidated_columns, top, corrected_bottom )]

        new_revised_dict_of_possible_values = build_dict_from_possible_rows_and_columns(revalidated_rows, revalidated_columns, cells)

        if check_for_answer(revised_dict_of_possible_values):
            break
        elif new_revised_dict_of_possible_values == revised_dict_of_possible_values:
            raise Exception("Solving Process Stalled.")
        else:
            revised_dict_of_possible_values = new_revised_dict_of_possible_values

    answer_result = render_dict_to_answer(revised_dict_of_possible_values)

    return answer_result

def solve_puzzle (clues):
    return solve(clues)