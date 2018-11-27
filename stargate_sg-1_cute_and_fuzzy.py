"""
Stargate SG-1: Cute and Fuzzy (Improved version) - (3 kyu)

Note: This kata is the improved/corrected version of this one.
I'm not the original author but, while the former has quit codewars without correcting the bugs in his kata and letting it inconsistent with the description, the latter took a lot of time to debug the thing and improve it (the original algorithm didn't have full coverage), so I published it on my side (and that will make the maintenance easier...).

Enjoy!



I don't even know what they look like. 
Furling... Sounds cute and fuzzy to me. 

- Jonas Quinn and Jack O'Neill, "Paradise Lost".


Previously on Stargate SG-1
Arriving on P4F-976, SG-1 finally come into contact with the Furlings, one of the four great races within the Milky Way. After several days of deliberation with the Furling Directorate, the Tauri finally have access to the knowledge they have been searching for.

The Furlings, having provided assistance with the Ancient's expansion into the Milky Way, have extensive knowledge of the Stargate Network and it's components. One such component, the Dial Home Device, has caused many disasters at Stargate Command through it's absence. Thankfully, the Furlings have all the necessary blueprints for it's construction, and have handed copies over to the Tauri. After beginning mass production of the control crystals necessary for it's function, Stargate Command has hit a snag. The Ancients had designed the control crystals to function if their inner pathways are as efficient as possible - essentially, the pathways must choose the shortest path between two nodes. Stargate Command has turned to you - a software engineer - to fix their problems.



Your Mission
Given a string containing the current state of the control crystals inner pathways (labeled as "X") and its gaps (labeled as "."), generate the shortest path from the start node (labeled as "S") to the goal node (labeled as "G") and return the new pathway (labeled with "P" characters).
If no solution is possible, return the string "Oh for crying out loud..." (in frustration).



The Rules
Nodes labeled as "X" are not traversable.
Nodes labeled as "." are traversable.
A pathway can be grown in eight directions (up, down, left, right, up-left, up-right, down-left, down-right), so diagonals are possible.
Nodes labeled "S" and "G" are not to be replaced with "P" in the case of a solution.
The shortest path is defined as the path with the shortest euclidiean distance going from one node to the next.
If several paths are possible with the same shortest distance, return any one of them.
Note that the mazes won't always be squares.


Example #1: Valid solution

.S...             .SP..
XXX..             XXXP.
.X.XX      =>     .XPXX
..X..             .PX..
G...X             G...X

Example #2: No solution

S....      
XX...      
...XX      =>     "Oh for crying out loud..."
.XXX.      
XX..G



Note: Your solution will have to be efficient because it will have to deal with a lot of maps and big ones.
Caracteristics of the random tests:

map sizes from 3x3 to 73x73 (step is 5 from one size to the other, mazes won't always be squares)
20 random maps for each size.
Overall, 311 tests to pass with the fixed ones.

"""

from collections import defaultdict
from math import sqrt
from time import time

def map_wires(existingWires):
    rows = existingWires.replace("\n", "-\n").split("\n")
    return dict({((x, y), n) for y, row in enumerate(rows) for x, n in enumerate(row)})

def find_neighbors(coord, valid_nodes):
    x, y = coord
    
    possibilities_straight = {(x+1, y),
                              (x-1, y),
                              (x, y+1),
                              (x, y-1)}

    possibilities_diagonal = {(x+1, y+1),
                              (x-1, y+1),
                              (x-1, y-1),
                              (x+1, y-1)}
    
    return possibilities_straight & valid_nodes, possibilities_diagonal & valid_nodes
    
def build_wiring_diagram(bread_crumb, crystal, goal, start):
    path = bread_crumb[goal]
    
    while path and path != start:
        crystal[path] = 'P'
        path = bread_crumb[path]
    
    return "".join([crystal[key] for key in sorted(crystal.keys(), key=lambda k:(k[1], k[0]))]).replace("-", "\n")

def wire_DHD_SG1(existingWires):
    x = time() + 0.29
    crystal = map_wires(existingWires)
    
    diagonal_distance = sqrt(2)
    
    start = None
    goal = None
    traversable = set()

    for coord, cell in crystal.items():
        if cell == '.':
            traversable.add(coord)
        elif cell == 'S':
            start = coord
        elif cell == 'G':
            goal = coord
            
    valid_nodes = traversable | { goal }

    big_val = float('inf')
    best_distance = defaultdict(lambda:big_val)
    
    best_distance[start] = 0

    bread_crumb = defaultdict(lambda: None)

    item_key_sorter = lambda k: k[1]
    most_promising_distance = 0

    visited = set()
    unvisited_leaves = {start: 0}

    while most_promising_distance < best_distance[goal] and unvisited_leaves != {}:
        if time() > x:
            q = existingWires.replace('\n','Q')
            raise Exception(q)

        most_promising_coord, most_promising_distance = min(unvisited_leaves.items(), key=item_key_sorter)

        valid_coords_straight, valid_coords_diagonal = find_neighbors(most_promising_coord, valid_nodes - visited)
        
        visited.add(most_promising_coord)
        _ = unvisited_leaves.pop(most_promising_coord)

        test_plots = {(crd, 1, most_promising_coord) for crd in valid_coords_straight} | {(crd, diagonal_distance, most_promising_coord) for crd in valid_coords_diagonal}

        for child_coord, distance, parent in test_plots:
            parent_best_distance = best_distance[parent]
            best_distance_candidate = parent_best_distance + distance
            
            if best_distance_candidate > best_distance[goal]:
                pass
            elif best_distance_candidate < best_distance[child_coord]:
                bread_crumb[child_coord] = parent
                best_distance[child_coord] = best_distance_candidate
                if child_coord not in visited:
                    unvisited_leaves[child_coord] = best_distance_candidate

    if goal in bread_crumb.keys():
        return build_wiring_diagram(bread_crumb, crystal, goal, start)
    else:
        return "Oh for crying out loud..."
