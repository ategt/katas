# coding: utf-8

"""
Plants and Zombies (3 kyu)
This kata is inspired by Plants vs. Zombies, a tower defense video game developed and originally published by PopCap Games.

The battlefield is the front lawn and the zombies are coming. Our defenses (consisting of pea-shooters) are in place and we've got the stats of each attacking zombie. Your job is to figure out how long it takes for them to penetrate our defenses.

Mechanics
The two images below represent the lawn (for the test example below) at separate stages in the game.
Left: state at move 3, before shooters fire. Right:state at move 5, after shooters fire. (Moves are 0-based)

example image
Moves: During a move, new zombies appear and/or existing ones move forward one space to the left. Then the shooters fire. This two-step process repeats.
If a zombie reaches a shooter's position, it destroys that shooter. In the example image above, the zombie at [4,4] on the left reaches the shooter at [4,2] and destroys it. The zombie has 1 health point remaining and is eliminated in the same move by the shooter at [4,0].
Numbered shooters shoot straight (to the right) a given number of times per move. In the example image, the green numbered shooter at [0,0] fires 2 times per move.
S-shooters shoot straight, and diagonally upward and downward (ie. three directions simultaneously) once per move. In the example image, the blue and orange S-shooters can attack zombies in any of the blue and orange squares, respectively (if not blocked by other zombies).
At move 3 the blue shooter can only hit the zombie at [1,5] while the orange shooter hits each of the zombies at [1,5], [2,7], and [4,6] once for that move.
Shooting Priority: The numbered shooters fire all their shots in a cluster, then the S-shooters fire their shots in order from right to left, then top to bottom. Note that once a zombie's health reaches 0 it drops immediately and does not absorb any additional shooter pellets.
In the example image, the orange S-shooter fires before the blue one.
Input
Your function will receive two arguments:

Lawn Map: An array/list consisting of strings, where each string represents a row of the map. Each string will consist of either " " (space character) which represents empty space, a numeric digit (0-9) representing a numbered shooter, or the letter S representing an S-shooter.
Zombie Stats: An array of subarrays representing each zombie, in the following format:
[i,row,hp] - where i is the move number (0-based) when it appears, row is the row the zombie walks down, and hp is the initial health point value of the zombie.
When new zombies appear, they start at the farthest right column of their row.
Input will always be valid.

Output
Return the number of moves before the first zombie penetrates our defenses (by getting past column 0), or null/None if all zombies are eliminated.

Test Example
lawn = [
    '2       ',
    '  S     ',
    '21  S   ',
    '13      ',
    '2 3     '
]
zombies = [[0,4,28],[1,1,6],[2,0,10],[2,4,15],[3,2,16],[3,3,13]]
plants_and_zombies(lawn,zombies); #10
For another Tower Defense-style challenge, check out Tower Defense: Risk Analysis

If you enjoyed this kata, be sure to check out my other katas.
--
You have an array of numbers.
Your task is to sort ascending odd numbers but even numbers must be on their places.

Zero isn't an odd number and you don't need to move it. If you have an empty array, you need to return it.

Example

sort_array([5, 3, 2, 8, 1, 4]) == [1, 3, 2, 8, 5, 4]


"""

def advance_zombies(zombies):
    local_zombies = clone_zombies(zombies)
    for zombie in local_zombies:
        zombie[0] -= 1
    return local_zombies

def determine_breach(zombies):
    return 0 < len(list(filter(lambda zombie: zombie[0] < 0, zombies)))

def destroy_occupied_shooters(lawn, zombies):
    new_rows = []
    for row_number, row in enumerate(lawn):
        new_row = "%s" % (row,)
        for column_number, cell in enumerate(row):
            if cell.isalnum():
                if len(list(filter(lambda zombie: zombie[0] == column_number and zombie[1] == row_number, zombies))) > 0:
                    new_row = new_row[:column_number] + ' ' + new_row[column_number+1:]

        new_rows.append(new_row)        
               
    return new_rows

def activated_zombies(move, zombies, lawn):
    actives = filter(lambda zombie: zombie[0] == move, zombies)
    actives = clone_zombies(actives)
    actives = [ [len(lawn[0]) - 1, zombie[1], zombie[2]] for zombie in actives]
    return actives

def direct_shooters_fire(lawn, active_zombies):
    local_zombies = clone_zombies(active_zombies)
    for row_number, row in enumerate(lawn):
        for shooter in row:
            if shooter.isnumeric():
                shots = int(shooter)
                
                zombies_in_row = list(filter(lambda zombie: zombie[1] == row_number, local_zombies))

                while shots > 0:
                    if len(zombies_in_row) > 0:
                        hp = zombies_in_row[0][2]
                        if hp > shots:
                            zombies_in_row[0][2] = hp - shots
                            print("Zombie getting hit by direct fire\tShots", shots, zombies_in_row[0], 'from', row)
                            shots = 0
                        else:
                            shots -= hp
                            eliminated_zombie = zombies_in_row.pop(0)
                            local_zombies = eliminate_zombie(local_zombies, eliminated_zombie)
                            print("Zombie eliminated by direct fire\t", eliminated_zombie)
                    else:
                        print("Direct fire missed - ", row_number, row)
                        shots = 0
                        
    return local_zombies

def clone_zombies(active_zombies):
    return [zombie.copy() for zombie in active_zombies]

def locate_s_shooters(lawn):
    strafers = []
    for row_number, row in enumerate(lawn):
        for column_number, cell in enumerate(row):
            if cell.isalpha():
                strafers.append({'row': row_number, 'column':column_number})
                
    return strafers                
            
def prioritize_s_shooters(s_shooters):
    return sorted(s_shooters, key=lambda item: item['column'] * 1000 - item['row'], reverse=True)
            
def angular_shooters_fire(row_number, column_number, active_zombies, lawn):
    local_zombies = clone_zombies(active_zombies)
    
    zombies_in_row = list(filter(lambda zombie: zombie[1] == row_number, local_zombies))
    
    forward_zombie = zombies_in_row[0] if len(zombies_in_row) > 0 else None

    upper_zombie = locate_zombie(lawn, row_number, column_number, local_zombies, next_coords_func=lambda row, column: (row-1,column+1))
    lower_zombie = locate_zombie(lawn, row_number, column_number, local_zombies, next_coords_func=lambda row, column: (row+1,column+1))

    zombies_getting_hit = [zombie for zombie in [lower_zombie, upper_zombie, forward_zombie] if zombie is not None and len(zombie) > 0]

    print("Zombies getting hit by angular fire", zombies_getting_hit)

    for zombie in zombies_getting_hit:
        hp = zombie[2]
        if hp > 1:
            zombie[2] -= 1
        else:
            local_zombies = eliminate_zombie(local_zombies, zombie)
            print("Zombie eliminated by angular fire\t", zombie)
            
    return local_zombies

def eliminate_zombie(local_zombies, eliminated_zombie):
    return [ *filter(lambda this_zombie: this_zombie != eliminated_zombie, local_zombies)]

def locate_zombie(lawn, row, column, zombies, next_coords_func):
    """
        # Zombie up one would be column_number + 1, row_number - 1
        next_coords_func = lambda 
    """
    zombie = None
    while zombie is None:
        row, column = next_coords_func(row, column)

        if row < 0 or row > len(lawn):
            break
        if column < 0 or column > len(lawn[0]):
            break

        zombie = [*filter(lambda zombie: zombie[1] == row and zombie[0] == column, zombies), None][0]
    return zombie

def run(lawn, zombies):
    " In the final version I removed the print statements, but I liked them here. "
    active_zombies = []
    moves = 0
    max_moves_required = max(map(lambda zombie: zombie[0], zombies))

    while moves <= max_moves_required or len(active_zombies) > 0:
        print("Beginning Move:", moves)
        active_zombies, lawn = play_turn(active_zombies, lawn, moves, zombies)

        # determine if zombies breached lawn
        if determine_breach(active_zombies):
            print("Breach!!!!!!!")
            return moves

        moves += 1

        display_battlefield(lawn, active_zombies, moves)
    
    print("All Zombies Eliminated.")

    return None

def play_turn(active_zombies, lawn, moves, zombies):
    lawn, active_zombies = play_zombies(active_zombies, lawn, moves, zombies)
    active_zombies = play_plants(lawn, active_zombies)

    return active_zombies, lawn

def play_plants(lawn, active_zombies):
    active_zombies = direct_shooters_fire(lawn, active_zombies)
    straffing_shooters = locate_s_shooters(lawn)
    straffing_shooters = prioritize_s_shooters(straffing_shooters)

    for shooter in straffing_shooters:
        active_zombies = angular_shooters_fire(shooter['row'], shooter['column'], active_zombies, lawn)
    return active_zombies

def play_zombies(active_zombies, lawn, moves, zombies):
    # advance existing zombies
    active_zombies = advance_zombies(active_zombies)

    # destroy shooters with zombies on top of them
    lawn = destroy_occupied_shooters(lawn, active_zombies)

    active_zombies = [*active_zombies , *activated_zombies(moves, zombies, lawn)]
    return lawn, active_zombies

def display_battlefield(lawn, active_zombies, turn):
    print("    '", "".join([str(i) if i < 10 else "+" for i in range(len(lawn[0]))]), "|  --", turn)

    for row_number, row in enumerate(lawn):
        these_zombies = filter(lambda zombie: zombie[1] == row_number, active_zombies)
        print("{}".format(row_number).rjust(3, ' '), "'", row, "|", list(these_zombies))
    print("")