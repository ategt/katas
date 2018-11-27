# coding: utf-8

import unittest

import plants_v_zombies

class TestPlantsVsZombies(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_example(self):
        lawn = [
            '2       ',
            '  S     ',
            '21  S   ',
            '13      ',
            '2 3     '
        ]
        zombies = [[0,4,28],[1,1,6],[2,0,10],[2,4,15],[3,2,16],[3,3,13]]

        breach_in = plants_v_zombies.run(lawn, zombies)
        self.assertEqual(breach_in, 10)

    def test_example2(self):
        lawn = [
			'11      ',
			' 2S     ',
			'11S     ',
			'3       ',
			'13      ']
        zombies = [[0,3,16],[2,2,15],[2,1,16],[4,4,30],[4,2,12],[5,0,14],[7,3,16],[7,0,13]]

        breach_in = plants_v_zombies.run(lawn, zombies)
        self.assertEqual(breach_in, 12)

    def test_example3(self):
        lawn = [
			'12        ',
			'3S        ',
			'2S        ',
			'1S        ',
			'2         ',
			'3         ']
        zombies = [[0,0,18],[2,3,12],[2,5,25],[4,2,21],[6,1,35],[6,4,9],[8,0,22],[8,1,8],[8,2,17],[10,3,18],[11,0,15],[12,4,21]]

        breach_in = plants_v_zombies.run(lawn, zombies)
        self.assertEqual(breach_in, 20)

    def test_example4(self):
        lawn = [
			'12      ',
			'2S      ',
			'1S      ',
			'2S      ',
			'3       ']
        zombies = [[0,0,15],[1,1,18],[2,2,14],[3,3,15],[4,4,13],[5,0,12],[6,1,19],[7,2,11],[8,3,17],[9,4,18],[10,0,15],[11,4,14]]

        breach_in = plants_v_zombies.run(lawn, zombies)
        self.assertEqual(breach_in, 19)

    def test_example5(self):
        lawn = [
			'1         ',
			'SS        ',
			'SSS       ',
			'SSS       ',
			'SS        ',
			'1         ']
        zombies = [[0,2,16],[1,3,19],[2,0,18],[4,2,21],[6,3,20],[7,5,17],[8,1,21],[8,2,11],[9,0,10],[11,4,23],[12,1,15],[13,3,22]]

        breach_in = plants_v_zombies.run(lawn, zombies)
        self.assertEqual(breach_in, None)

    def test_example_image(self):
        lawn = [
			'2       ',
			'  S     ',
			'21  S   ',
			'13      ',
			'2 3     ']
        zombies = [[0,4,23],[1,1,6],[2,0,10],[2,4,20],[3,2,16],[3,3,13]]

        breach_in = plants_v_zombies.run(lawn, zombies)
        self.assertEqual(breach_in, None)

    def test_example_image_shooters(self):
        lawn = [
			'2       ',
			'  S     ',
			'21  S   ',
			'13      ',
			'2 3     ']
        zombies = [[4,4,11],[5,1,4],[6,0,8],[6,4,15],[7,2,16],[7,3,13]]

        active_zombies = plants_v_zombies.direct_shooters_fire(lawn, zombies)

        self.assertEqual(active_zombies, [[4,4,6],[5,1,4],[6,0,6],[6,4,15],[7,2,13],[7,3,9]])

        # Organize Angular Shooters
        straffing_shooters = plants_v_zombies.locate_s_shooters(lawn)
        straffing_shooters = plants_v_zombies.prioritize_s_shooters(straffing_shooters)

        # Fire Angular Shooters
        for shooter in straffing_shooters:
            active_zombies = plants_v_zombies.angular_shooters_fire(shooter['row'], shooter['column'], active_zombies, lawn)
        
        self.assertEqual(active_zombies, [[4,4,6],[5,1,2],[6,0,6],[6,4,14],[7,2,12],[7,3,9]])

    def test_custom_angular_shooters(self):
        lawn = [
			'    ',
			'    ',
			'S   ',
			'    ',
			'    ']
        zombies = [[2,0,4],[2,1,4],[2,2,4],[2,3,4],[2,4,4]]

        # Organize Angular Shooters
        straffing_shooters = plants_v_zombies.locate_s_shooters(lawn)
        straffing_shooters = plants_v_zombies.prioritize_s_shooters(straffing_shooters)

        # Fire Angular Shooters
        for shooter in straffing_shooters:
            zombies = plants_v_zombies.angular_shooters_fire(shooter['row'], shooter['column'], zombies, lawn)
        
        self.assertEqual(zombies, [[2,0,3],[2,1,4],[2,2,3],[2,3,4],[2,4,3]])

    def test_example_image_iso(self):
        lawn = [
			'2       ',
			'  S     ',
			'21  S   ',
			'13      ',
			'2 3     ']
        zombies = [[4,4,11],[5,1,4],[6,0,8],[6,4,15],[7,2,16],[7,3,13]]

        # Second part of turn 3
        iso_zombies = plants_v_zombies.play_plants(lawn, zombies)

        self.assertEqual(iso_zombies, [[4,4,6],[5,1,2],[6,0,6],[6,4,14],[7,2,12],[7,3,9]])

        # Turn 4A
        lawn, A4_zombies = plants_v_zombies.play_zombies(iso_zombies, lawn, 4, [])

        # Turn 4B
        B4_zombies = plants_v_zombies.play_plants(lawn, A4_zombies)

        # Turn 5A
        lawn, A5_zombies = plants_v_zombies.play_zombies(B4_zombies, lawn, 5, [])

        self.assertEqual(lawn, ['2       ', '  S     ', '21  S   ', '13      ', '2       '])
        self.assertEqual(A5_zombies, [[2,4,1],[3,1,1],[4,0,4],[4,4,13],[5,2,8],[5,3,5]])

        # Turn 5B
        B5_zombies = plants_v_zombies.play_plants(lawn, A5_zombies)

        #self.assertEqual(active_zombies, [[2, 4, 6], [3, 1, 3], [4, 0, 6], [4, 4, 14], [5, 2, 12], [5, 3, 9]])

        self.assertEqual(B5_zombies, [[4,0,2],[4,4,12],[5,2,4]])

    def test_possible_bug(self):
        lawn = ['2       ', 
                '  S     ', 
                '21  S   ', 
                '13      ', 
                '2       ']
        zombies = [[2,4,1],[3,1,1],[4,0,4],[4,4,13],[5,2,8],[5,3,5]]

        zombies = plants_v_zombies.direct_shooters_fire(lawn, zombies)

        self.assertEqual(zombies, [[3, 1, 1], [4, 0, 2], [4, 4, 12], [5, 2, 5], [5, 3, 1]])

        # Organize Angular Shooters
        straffing_shooters = plants_v_zombies.locate_s_shooters(lawn)
        straffing_shooters = plants_v_zombies.prioritize_s_shooters(straffing_shooters)

        self.assertEqual(straffing_shooters, [{'column': 4, 'row': 2}, {'column': 2, 'row': 1}])

        # Fire Angular Shooters
        for shooter in straffing_shooters:
            zombies = plants_v_zombies.angular_shooters_fire(shooter['row'], shooter['column'], zombies, lawn)

        self.assertEqual(zombies, [[4,0,2],[4,4,12],[5,2,4]])

    def test_possible_bug_b(self):
        lawn = ['2       ', 
                '  S     ', 
                '21  S   ', 
                '13      ', 
                '2       ']
        zombies = [[3, 1, 1], [4, 0, 2], [4, 4, 12], [5, 2, 5], [5, 3, 1]]
        
        angular1 = {'column': 4, 'row': 2}
        angular2 = {'column': 2, 'row': 1}

        zombies = plants_v_zombies.angular_shooters_fire(angular1['row'], angular1['column'], zombies, lawn)

        self.assertEqual(zombies, [[3, 1, 1], [4, 0, 2], [4, 4, 12], [5, 2, 4]])
        
        zombies = plants_v_zombies.angular_shooters_fire(angular2['row'], angular2['column'], zombies, lawn)        
        
        self.assertEqual(zombies, [[4,0,2],[4,4,12],[5,2,4]])

    def test_example6(self):
        lawn = [
			'SSS',
			'SSS',
			'SSS']
        straffing_shooters = plants_v_zombies.locate_s_shooters(lawn)
        straffing_shooters = plants_v_zombies.prioritize_s_shooters(straffing_shooters)
        
        self.assertEqual(straffing_shooters, [{'column': 2, 'row': 0}, {'column': 2, 'row': 1}, {'column': 2, 'row': 2}, {'column': 1, 'row': 0}, {'column': 1, 'row': 1}, {'column': 1, 'row': 2}, {'column': 0, 'row': 0}, {'column': 0, 'row': 1}, {'column': 0, 'row': 2}])

    def test_example_x(self):
        lawn = ['2 2 3  S                ', 
                ' 1 3 1                  ', #
                '3 1  S                  ', 
                '11  4   S               ', 
                '22   S  S               ', 
                '3 1 2 S                 ', 
                '4    S                  ', #
                '1 1 1 1                 ', 
                '1 S 3                   ', 
                '1 S 2                   ', #
                '4      S                ', 
                '2 4 2   S               ', 
                '4       1               ', #
                '3 1S1                   ', 
                '4   S  2                ', 
                '11 3 S 2                ']
        zombies = [[0, 0, 96], 
                   [0, 3, 75], 
                   [0, 7, 82], 
                   [0, 12, 98],
                   [0, 14, 104], 
                   [2, 5, 102], 
                   [2, 6, 51], 
                   [2, 8, 56], 
                   [3, 1, 74], 
                   [3, 2, 65], 
                   [3, 3, 58], 
                   [3, 4, 85], 
                   [3, 9, 44], 
                   [3, 10, 60],
                   [4, 14, 63], 
                   [4, 11, 91], 
                   [5, 13, 120], 
                   [5, 15, 26], 
                   [7, 1, 43], 
                   [7, 6, 38], 
                   [7, 9, 61], 
                   [7, 12, 64], 
                   [9, 0, 69], 
                   [9, 2, 37], 
                   [9, 14, 51], 
                   [10, 3, 84], 
                   [10, 7, 68], 
                   [10, 8, 82], 
                   [10, 11, 77], 
                   [10, 15, 101], 
                   [12, 4, 100], 
                   [13, 5, 70], 
                   [13, 6, 76], 
                   [14, 7, 54]]

        breach_in = plants_v_zombies.run(lawn, zombies)
        self.assertEqual(breach_in, 31)

if __name__ == '__main__':
    unittest.main()