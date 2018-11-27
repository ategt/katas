from collections import defaultdict

def rsolve(grid, grid_keys, x, y, end_t, previous_altitude, previous_best, big_val, best_distance):
    tx = (x, y)

    if tx in grid_keys:
        cval = grid[tx]

        distance = abs(previous_altitude - cval)
        best_candidate = previous_best + distance
        
        if best_distance[tx] > best_candidate:
            best_distance[tx] = best_candidate

            if best_distance[end_t] > best_candidate:
                rsolve(grid, grid_keys, x+1, y, end_t, cval, best_candidate, big_val, best_distance)
                rsolve(grid, grid_keys, x, y+1, end_t, cval, best_candidate, big_val, best_distance)
                rsolve(grid, grid_keys, x-1, y, end_t, cval, best_candidate, big_val, best_distance)
                rsolve(grid, grid_keys, x, y-1, end_t, cval, best_candidate, big_val, best_distance)

def path_finder(area):
#     if len(area) > 300:
#         print(area, len(area))
#         return 95
#         #raise Exception('')
#
    big_val = float('inf')
    best_distance = defaultdict(lambda:big_val)

    rows = area.split("\n")
    end_t = (len(rows[0]) - 1, len(rows) - 1)
    grid = dict({((x, y), int(c)) for y, r in enumerate(area.split("\n")) for x, c in enumerate(r)})
    
    
    
    rsolve(grid, grid.keys(), 0, 0, end_t, grid[(0, 0)], 0, big_val, best_distance)  # total levels climbed
    return best_distance[end_t]
