# coding: utf-8

from itertools import permutations

def setup_visual_possibilities(grid_side_length):
    return [*[(visible(i), visible(reversed(i)), i) for i in permutations([i for i in range(1, grid_side_length + 1)])],
            *[(0, visible(reversed(i)), i) for i in permutations([i for i in range(1, grid_side_length + 1)])],
            *[(visible(i), 0, i) for i in permutations([i for i in range(1, grid_side_length + 1)])],
            *[(0, 0, i) for i in permutations([i for i in range(1, grid_side_length + 1)])]]

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

def line_valid(line, grid_size):
    return len(set(line)) == grid_size

def build_rows(y, current_possibles, grid_size):
    return list(map(lambda item: item, filter(lambda item: item is not None and len(item) == grid_size, _build_rows(x=0, y=y, current_possibles = current_possibles, grid_size = grid_size))))

def build_colums(x, current_possibles, grid_size):
    return list(map(lambda item: item, filter(lambda item: item is not None and len(item) == grid_size, _build_colum(x=x, y=0, current_possibles = current_possibles, grid_size = grid_size))))

def _build_colum(x, y, current_possibles, grid_size):
    possible_values = current_possibles.get((x, y), [])

    if y >= grid_size:
        return [None]

    results = [[value] if remainder is None else [value, *remainder] for value in possible_values for remainder in _build_colum(x=x, y=y+1, current_possibles=current_possibles, grid_size=grid_size)]

    return results

def _build_rows(x, y, current_possibles, grid_size):
    possible_values = current_possibles.get((x, y), [])

    if x >= grid_size:
        return [None]

    results = [[value] if remainder is None else [value, *remainder] for value in possible_values for remainder in _build_rows(x=x+1, y=y, current_possibles=current_possibles, grid_size=grid_size)]

    return results

def validate_row(y, current_possibles, left_and_right, grid_size):
    possible_row_permutations = build_rows(y=y, current_possibles = current_possibles, grid_size=grid_size)
    l, r = left_and_right[y]
    return [row_canidate for row_canidate in possible_row_permutations if line_with_bounds_possible(row_canidate, l, r)]

def validate_column(x, current_possibles, top_and_bottom, grid_size):
    possible_column_permutations = build_colums(x=x, current_possibles = current_possibles, grid_size=grid_size)
    t, b = top_and_bottom[x]
    return [column_canidate for column_canidate in possible_column_permutations if line_with_bounds_possible(column_canidate, t, b)]

def build_dict_from_possible_rows_and_columns(possible_rows, possible_columns, cells):
    "dict_of_possible_values"
    return dict(((x,y), {possible_colum[y] for possible_colum in possible_columns[x]} & {possible_row[x] for possible_row in possible_rows[y]}) for x, y in cells)

def render_dict_to_answer(answer_dict, grid_size, desired_output):
    return desired_output(desired_output(answer_dict[(x, y)].pop() for x in range(0, grid_size)) for y in range(0, grid_size))

def check_for_answer(answer_dict, grid_size):
    return len({len(answer_dict[(x, y)]) for x in range(0, grid_size) for y in range(0, grid_size)}) == 1

def possible_lines(towers_visible, opposite_side_towers_visible, vis_pos_list):
        return list(map(lambda tpl: tpl[2], filter(lambda tpl: tpl[0] == towers_visible and tpl[1] == opposite_side_towers_visible, vis_pos_list)))

def line_with_bounds_possible(line, l, r):
    return ( l == 0 or visible(line) == l ) and ( r == 0 or visible(reversed(line)) == r )

def validate_columns(possible_x_columns):
    return [tuple(filter(line_valid, column_candidates)) for column_candidates in possible_x_columns]

def validate_rows(possible_x_rows):
    return [tuple(filter(line_valid, row_candidates)) for row_candidates in possible_x_rows]

def split_dictionary_into_rows(dict_of_possible_values, grid_size, corrected_left, right):
    possible_x_rows    = [build_rows(i, dict_of_possible_values, grid_size) for i in range(grid_size)]

    revalidated_rows = validate_lines(possible_x_rows, grid_size)
    revalidated_rows = [[row_canidate for row_canidate in possible_row_permutations if line_with_bounds_possible(row_canidate, l, r)] for possible_row_permutations, l, r in zip(revalidated_rows, corrected_left, right )]

    return revalidated_rows

def split_dictionary_into_columns(dict_of_possible_values, grid_size, top, corrected_bottom):
    possible_x_columns = [build_colums(i, dict_of_possible_values, grid_size) for i in range(grid_size)]

    revalidated_columns = validate_lines(possible_x_columns, grid_size)
    revalidated_columns = [[column_canidate for column_canidate in possible_column_permutations if line_with_bounds_possible(column_canidate, t, b)] for possible_column_permutations, t, b in zip(revalidated_columns, top, corrected_bottom )]

    return revalidated_columns

def split_dictionary_into_rows_and_columns(dict_of_possible_values, grid_size, corrected_left, right, top, corrected_bottom):
    revalidated_rows = split_dictionary_into_rows(dict_of_possible_values, grid_size, corrected_left, right)
    revalidated_columns = split_dictionary_into_columns(dict_of_possible_values, grid_size, top, corrected_bottom)

    return revalidated_rows, revalidated_columns

def validate_side_of_lines(side_of_line_candidates_collection, grid_size):
    return [validate_lines(line_candidates_collection, grid_size) for line_candidates_collection in side_of_line_candidates_collection]

def validate_lines(line_candidates_collection, grid_size):
    local_line_valid = lambda x: line_valid(x, grid_size)
    return [filter(local_line_valid, line_candidates) for line_candidates in line_candidates_collection]

def solve(clues, grid_size = 6, desired_output=tuple):
    vis_pos_list = setup_visual_possibilities(grid_size)
    top, right, bottom, left = breakup_clues(clues, grid_size)

    right, corrected_left = right, list(reversed(left))
    left_and_right = list(zip(corrected_left, right))

    top, corrected_bottom = top, list(reversed(bottom))
    top_and_bottom = list(zip(top,corrected_bottom))

    cells = {(x, y) for y in range(0, grid_size) for x in range(0, grid_size)}

    possible_rows = [possible_lines(x, y, vis_pos_list) for x,y in left_and_right]
    possible_columns = [possible_lines(x, y, vis_pos_list) for x,y in top_and_bottom]

    dict_of_possible_values = build_dict_from_possible_rows_and_columns(possible_rows, possible_columns, cells)

    validated_rows, validated_columns = split_dictionary_into_rows_and_columns(dict_of_possible_values, grid_size, corrected_left, right, top, corrected_bottom)

    revised_dict_of_possible_values = build_dict_from_possible_rows_and_columns(validated_rows, validated_columns, cells)

    for _ in range(50):
        revalidated_rows, revalidated_columns = split_dictionary_into_rows_and_columns(revised_dict_of_possible_values, grid_size, corrected_left, right, top, corrected_bottom)

        new_revised_dict_of_possible_values = build_dict_from_possible_rows_and_columns(revalidated_rows, revalidated_columns, cells)

        if check_for_answer(revised_dict_of_possible_values, grid_size):
            break
        elif new_revised_dict_of_possible_values == revised_dict_of_possible_values:
            raise Exception("Solving Process Stalled.")
        else:
            revised_dict_of_possible_values = new_revised_dict_of_possible_values

    answer_result = render_dict_to_answer(revised_dict_of_possible_values, grid_size, desired_output)

    return answer_result