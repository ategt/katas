"""
Monty Hall Simulation

On the TV Game Show 'Let's Make a Deal' each contestant tries to figure out which one of three doors contains a prize.  The host, Monty Hall, would ask them to pick 
one, then he would reveal one of the doors the contestant did not choose.  This revealed door never contained the prize.  Monty Hall would then ask the contestant if they 
would like to switch to the other door.

The chances of the contestant winning are not the same for staying and switching.  Use code to determine which is the better choice.
"""

import random

DOOR_COLORS = ["Red", "Blue", "Green"]

def simulate_game(door_colors=DOOR_COLORS):
    doors = [{'color': door_color, 'has_prize':False, 'is_open':False, 'player_choosen':False} for door_color in door_colors]

    random.shuffle(doors)

    doors[0]['has_prize'] = True
    prize_door = doors[0]

    random.shuffle(doors)

    doors[0]['player_choosen'] = True
    player_door = doors[0]

    doors_without_a_prize = filter(lambda door: door['has_prize'] == False, doors)
    doors_eligible_for_opening = list(filter(lambda door: door['player_choosen'] == False, doors_without_a_prize))

    random.shuffle(doors_eligible_for_opening)

    doors_eligible_for_opening[0]['is_open'] = True
    open_door = doors_eligible_for_opening[0]

    other_door = list(filter(lambda door: door['is_open'] == False and door['player_choosen'] == False, doors))[0]

    story = """Monty Hall asks the player to choose a door.  The player chooses the {0} colored door.  Then Monty Hall opens the {1} door to reveal that it is empty.  Monty Hall then asks the player if they would like to switch their choosen door, {0}, for the {2} colored door, which is the only other door in play.  

And while the player ponders their decision, which will decide whether they win or lose, Monty Hall already knows that the prize is behind the {3} door. If the player stays they will {4} and if the player switches they will {5}.""".format(player_door['color'], open_door['color'], other_door['color'], prize_door['color'], "win" if player_door == prize_door else "lose", "win" if player_door != prize_door else "lose")
    
    
    return story, 1 if player_door == prize_door else 0, 1 if player_door != prize_door else 0

if __name__ == '__main__':
    story, stay, switch = simulate_game(DOOR_COLORS)

    print(story)
    print("Stay", stay, "\tSwitch", switch)