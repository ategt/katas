import unittest

import json

from boggle import find_word

class TestBoggle(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run(self):
        testBoard = [
            ["E","A","R","A"],
            ["N","L","E","C"],
            ["I","A","I","S"],
            ["B","Y","O","R"]
            ]

        self.assertEqual( find_word(testBoard, "C"               ), True  , "Test for C")
        self.assertEqual( find_word(testBoard, "EAR"             ), True  , "Test for EAR")
        self.assertEqual( find_word(testBoard, "EARS"            ), False , "Test for EARS")
        self.assertEqual( find_word(testBoard, "BAILER"          ), True  , "Test for BAILER")
        self.assertEqual( find_word(testBoard, "RSCAREIOYBAILNEA"), True  , "Test for RSCAREIOYBAILNEA")
        self.assertEqual( find_word(testBoard, "CEREAL"          ), False , "Test for CEREAL")
        self.assertEqual( find_word(testBoard, "ROBES"           ), False , "Test for ROBES")

if __name__ == '__main__':
    unittest.main()