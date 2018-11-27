# coding: utf-8

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
                    # print("Destroying shooter ", lawn[row_number][column_number], "at ", row_number, column_number)
                    # print("Changing ", cell, "from", "'%s'" % (row,), 'to', "'%s'" % (new_row,))

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