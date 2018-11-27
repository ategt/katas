import unittest

import json

from towers_kata import solve as solve_puzzle

class TestTowers(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_solve(self):
        clues = [7,0,0,0,2,2,3, 0,0,3,0,0,0,0, 3,0,3,0,0,5,0, 0,0,0,0,5,0,4]
        
        expected = [ [1,5,6,7,4,3,2],
                        [2,7,4,5,3,1,6],
                        [3,4,5,6,7,2,1],
                        [4,6,3,1,2,7,5],
                        [5,3,1,2,6,4,7],
                        [6,2,7,3,1,5,4],
                        [7,1,2,4,5,6,3] ]
                    
        actual = solve_puzzle (clues, 7, list)

        self.assertEqual(actual, expected)

    def test_solve_2(self):
        clues = [0,2,3,0,2,0,0, 5,0,4,5,0,4,0, 0,4,2,0,0,0,6, 5,2,2,2,2,4,1]
                
        expected = [ [7,6,2,1,5,4,3],
                        [1,3,5,4,2,7,6],
                        [6,5,4,7,3,2,1],
                        [5,1,7,6,4,3,2],
                        [4,2,1,3,7,6,5],
                        [3,7,6,2,1,5,4],
                        [2,4,3,5,6,1,7] ]
                    
        actual = solve_puzzle (clues, 7, list)

        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()