import unittest

from booleanorder import solve

class TestBooleanOrder(unittest.TestCase):
 
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_first_example(self):
        print(solve("tft","^&"), 2)
        print(solve("ttftff","|&^&&"),16)
        print(solve("ttftfftf","|&^&&||"),339)
        print(solve("ttftfftft","|&^&&||^"),851)
        print(solve("ttftfftftf","|&^&&||^&"),2434)


        self.assertEqual(solve("tft","^&"), 2)
        self.assertEqual(solve("ttftff","|&^&&"),16)
        self.assertEqual(solve("ttftfftf","|&^&&||"),339)
        self.assertEqual(solve("ttftfftft","|&^&&||^"),851)
        self.assertEqual(solve("ttftfftftf","|&^&&||^&"),2434)

if __name__ == '__main__':
    unittest.main()