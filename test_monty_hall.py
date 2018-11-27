import unittest

from monty_hall import simulate_game

import time
import math

class TestMontyHall(unittest.TestCase):
 
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def countDigits(self, number):
        " SO - https://stackoverflow.com/questions/2189800/length-of-an-integer-in-python "
        return int(math.log10(number))+1

    def test_run_simulate_many_times(self):
        t = time.time()
        running_stay, running_switch = 0, 0

        simulations = 1_000_000

        for _ in range(simulations):
            story, stay, switch = simulate_game()

            self.assertIsNotNone(story)
            
            running_stay += stay
            running_switch += switch

            self.assertNotEqual(stay, switch)

        t = time.time() - t

        print("Simulation run", simulations, "times in ", t, "seconds.")

        self.assertEqual(running_stay + running_switch, simulations)

        # By my math, switching should have twice the success rate of staying.
        # ( plus or minus twenty percent )
        self.assertTrue( running_switch - running_switch * .20 < running_stay * 2 < running_switch + running_switch * .20)


if __name__ == '__main__':
    unittest.main()