"""
Path Finder #3: the Alpinist (3 kyu)

Task
You are at start location [0, 0] in mountain area of NxN and you can only move in one of the four cardinal directions (i.e. North, East, South, West). Return minimal number of climb rounds to target location [N-1, N-1]. Number of climb rounds between adjacent locations is defined as difference of location altitudes (ascending or descending).

Location altitude is defined as an integer number (0-9).
"""

from collections import defaultdict

def upate_best_distance(x, y, r, c, previous_altitude, previous_best, best_distance, grid, grid_keys, still_updating):
    tx = (x+r, y+c)
    if tx in grid_keys:
        current_altitude = grid[tx]
        distance = abs(previous_altitude - current_altitude)
        best_candidate = previous_best + distance
        
        if best_distance[tx] > best_candidate:
            best_distance[tx] = best_candidate
            still_updating.add(True)

def path_finder(area):
    big_val = float('inf')
    best_distance = defaultdict(lambda:big_val)
    
    best_distance[(0, 0)] = 0

    rows = area.split("\n")
    size = len(rows)
    end_tuple = (size - 1, size - 1)

    grid = dict({((x, y), int(c)) for y, r in enumerate(rows) for x, c in enumerate(r)})

    keys = grid.keys()
    
    still_updating = {False, True}

    while True in still_updating:
        still_updating.clear()
        for y in range(size):
            for x in range(size):
                current_tuple = (x, y)
                current_altitude = grid[current_tuple]
                current_best = best_distance[current_tuple]
                upate_best_distance(x, y,  1,  0, current_altitude, current_best, best_distance, grid, keys, still_updating)
                upate_best_distance(x, y,  0,  1, current_altitude, current_best, best_distance, grid, keys, still_updating)
                upate_best_distance(x, y, -1,  0, current_altitude, current_best, best_distance, grid, keys, still_updating)
                upate_best_distance(x, y,  0, -1, current_altitude, current_best, best_distance, grid, keys, still_updating)

    return best_distance[end_tuple]