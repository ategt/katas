import unittest

import json

from towers_kata import build_rows, validate_row, setup_visual_possibilities, possible_lines, breakup_clues, build_dict_from_possible_rows_and_columns, validate_columns, validate_rows, split_dictionary_into_rows_and_columns, render_dict_to_answer, check_for_answer, solve

class TestTowers(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run(self):
        xpossibles = {(0, 0): {1, 2},
                        (0, 1): {4},
                        (0, 2): {2, 3},
                        (0, 3): {1, 2},
                        (1, 0): {2, 3},
                        (1, 1): {1, 2},
                        (1, 2): {4},
                        (1, 3): {1, 3},
                        (2, 0): {4},
                        (2, 1): {1, 2},
                        (2, 2): {2},
                        (2, 3): {3},
                        (3, 0): {1, 2},
                        (3, 1): {3},
                        (3, 2): {1, 2},
                        (3, 3): {4}}

        results = build_rows(0, xpossibles, 4)

        self.assertEqual( results, [[1, 2, 4, 1],
                                    [1, 2, 4, 2],
                                    [1, 3, 4, 1],
                                    [1, 3, 4, 2],
                                    [2, 2, 4, 1],
                                    [2, 2, 4, 2],
                                    [2, 3, 4, 1],
                                    [2, 3, 4, 2]])

    def test_vispos(self):
        grid_size = 4
        vis_pos_list = setup_visual_possibilities(grid_size)

        clues = (
                2, 2, 1, 3,
                2, 2, 3, 1,
                1, 2, 2, 3,
                3, 2, 1, 3 )

        top, right, bottom, left = breakup_clues(clues, 4)

        right, corrected_left = right, list(reversed(left))
        left_and_right = list(zip(corrected_left, right))

        top, corrected_bottom = top, list(reversed(bottom))
        top_and_bottom = list(zip(top,corrected_bottom))

        cells = {(x, y) for y in range(0, 4) for x in range(0, 4)}

        possible_rows = possible_lines(left_and_right[0][0], left_and_right[0][1], vis_pos_list)

        self.assertEqual(possible_rows, [(1, 2, 4, 3), (1, 3, 4, 2), (2, 3, 4, 1)])

        possible_rows = [possible_lines(x, y, vis_pos_list) for x,y in left_and_right]
        possible_columns = [possible_lines(x, y, vis_pos_list) for x,y in top_and_bottom]

        self.assertEqual(possible_rows, [[(1, 2, 4, 3), (1, 3, 4, 2), (2, 3, 4, 1)],
                                        [(4, 1, 2, 3), (4, 2, 1, 3)],
                                        [(1, 4, 3, 2), (2, 4, 3, 1), (3, 4, 2, 1)],
                                        [(1, 3, 2, 4), (2, 1, 3, 4), (2, 3, 1, 4)]])

        self.assertEqual(possible_columns, [[(1, 4, 3, 2), (2, 4, 3, 1), (3, 4, 2, 1)],
                                            [(1, 4, 2, 3), (2, 1, 4, 3), (2, 4, 1, 3), (3, 1, 4, 2), (3, 2, 4, 1), (3, 4, 1, 2)],
                                            [(4, 1, 2, 3), (4, 2, 1, 3)],
                                            [(1, 3, 2, 4), (2, 1, 3, 4), (2, 3, 1, 4)]])

        dict_of_possible_values = build_dict_from_possible_rows_and_columns(possible_rows, possible_columns, cells)

        self.assertEqual(dict_of_possible_values, {(0, 0): {1, 2},
                                                    (0, 1): {4},
                                                    (0, 2): {2, 3},
                                                    (0, 3): {1, 2},
                                                    (1, 0): {2, 3},
                                                    (1, 1): {1, 2},
                                                    (1, 2): {4},
                                                    (1, 3): {1, 3},
                                                    (2, 0): {4},
                                                    (2, 1): {1, 2},
                                                    (2, 2): {2},
                                                    (2, 3): {3},
                                                    (3, 0): {1, 2},
                                                    (3, 1): {3},
                                                    (3, 2): {1, 2},
                                                    (3, 3): {4}})

        validated_rows, validated_columns = split_dictionary_into_rows_and_columns(dict_of_possible_values, grid_size)

        revised_dict_of_possible_values = build_dict_from_possible_rows_and_columns(validated_rows, validated_columns, cells)

        self.assertFalse(check_for_answer(revised_dict_of_possible_values, grid_size))

        revalidated_rows, revalidated_columns = split_dictionary_into_rows_and_columns(revised_dict_of_possible_values, grid_size)

        revised_dict_of_possible_values = build_dict_from_possible_rows_and_columns(revalidated_rows, revalidated_columns, cells)

        self.assertTrue(check_for_answer(revised_dict_of_possible_values, grid_size))

        self.assertEqual(revised_dict_of_possible_values, {(0, 0): {1},
                                                            (0, 1): {4},
                                                            (0, 2): {3},
                                                            (0, 3): {2},
                                                            (1, 0): {3},
                                                            (1, 1): {2},
                                                            (1, 2): {4},
                                                            (1, 3): {1},
                                                            (2, 0): {4},
                                                            (2, 1): {1},
                                                            (2, 2): {2},
                                                            (2, 3): {3},
                                                            (3, 0): {2},
                                                            (3, 1): {3},
                                                            (3, 2): {1},
                                                            (3, 3): {4}})

        answer_result = render_dict_to_answer(revised_dict_of_possible_values, grid_size, tuple)

        expected_answer = ( ( 1, 3, 4, 2 ),
                            ( 4, 2, 1, 3 ),
                            ( 3, 4, 2, 1 ),
                            ( 2, 1, 3, 4 ) )

        self.assertEqual(answer_result, expected_answer)                            

    def test_solve(self):
        clues = ( 0, 0, 1, 2,   
                    0, 2, 0, 0,   
                    0, 3, 0, 0, 
                    0, 1, 0, 0 )

        answer = solve(clues, 4)

        self.assertEqual(answer, ( ( 2, 1, 4, 3 ), 
                                    ( 3, 4, 1, 2 ), 
                                    ( 4, 2, 3, 1 ), 
                                    ( 1, 3, 2, 4 ) ))

if __name__ == '__main__':
    unittest.main()