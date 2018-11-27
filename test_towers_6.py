import unittest

import json

from towers_kata import solve as solve_puzzle

class TestTowers(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_solve(self):
        clues = ( 3, 2, 2, 3, 2, 1,
                1, 2, 3, 3, 2, 2,
                5, 1, 2, 2, 4, 3,
                3, 2, 1, 2, 2, 4)
                
        expected = (( 2, 1, 4, 3, 5, 6 ),
                    ( 1, 6, 3, 2, 4, 5 ),
                    ( 4, 3, 6, 5, 1, 2 ),
                    ( 6, 5, 2, 1, 3, 4 ),
                    ( 5, 4, 1, 6, 2, 3 ),
                    ( 3, 2, 5, 4, 6, 1 ))
                    
        actual = solve_puzzle (clues, 6)

        self.assertEqual(actual, expected)

    def test_solve_2(self):
        clues = ( 0, 0, 0, 2, 2, 0,
                0, 0, 0, 6, 3, 0,
                0, 4, 0, 0, 0, 0,
                4, 4, 0, 3, 0, 0)
                
        expected = (( 5, 6, 1, 4, 3, 2 ), 
                    ( 4, 1, 3, 2, 6, 5 ), 
                    ( 2, 3, 6, 1, 5, 4 ), 
                    ( 6, 5, 4, 3, 2, 1 ), 
                    ( 1, 2, 5, 6, 4, 3 ), 
                    ( 3, 4, 2, 5, 1, 6 ))
                    
        actual = solve_puzzle (clues, 6)

        self.assertEqual(actual, expected)

    def test_solve_3(self):
        clues = ( 0, 3, 0, 5, 3, 4, 
                0, 0, 0, 0, 0, 1,
                0, 3, 0, 3, 2, 3,
                3, 2, 0, 3, 1, 0)
                
        expected = (( 5, 2, 6, 1, 4, 3 ), 
                    ( 6, 4, 3, 2, 5, 1 ), 
                    ( 3, 1, 5, 4, 6, 2 ), 
                    ( 2, 6, 1, 5, 3, 4 ), 
                    ( 4, 3, 2, 6, 1, 5 ), 
                    ( 1, 5, 4, 3, 2, 6 ))
                    
        actual = solve_puzzle (clues, 6)

        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()