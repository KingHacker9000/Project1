"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""

# Note: You may add in other import statements here as needed
from game_data import World, Item, Location, Player

MOVES_PER_TURN = 3
BACK_STORY = """"""
RULES = ("=" * 40) + """\n"""

if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))

    p1 = Player("Player 1", 0, 2)  # set starting location of player; you may change the x, y coordinates here as appropriate
    p2 = Player("Player 2", 0, 4)

    menu = ["Look", "Inventory", "Score", "Quit", "Rules"]

    current_player = p1

    print(BACK_STORY)
    print(RULES)

    while not p1.victory and not p2.victory:

        print('#'*30)
        print(current_player.name + "'s Turn")
        print('#'*30)

        location = w.get_location(current_player.x, current_player.y)

        if location.visited:
            print(location.b_description)
        else:
            print(location.l_description, location.position)
            location.visited = True

        print("What to do? \n")
        print("[menu]")
        for action in location.available_actions():
            print(action)

        choice = input("\nEnter action: ").capitalize().strip()

        while choice in menu + ['[menu]'] and choice not in location.available_actions():

            if choice == "[menu]":
                print("Menu Options: \n")
                for option in menu:
                    print(option)

            elif choice == 'Look':
                print("Looking")

            elif choice == 'Inventory':
                print(current_player.inventory)

            elif choice == "Score":
                print(current_player.score)

            elif choice == "Quit":
                print("GAME OVER!!")
                exit()

            elif choice == "Rules":
                print(RULES)

            else:
                print('NOT A VALID ACTION!')

            for action in location.available_actions():
                print(action)

            choice = input("\nChoose action: ")

        if choice in ['North', 'Up']:
            current_player.y -= 1

        elif choice in ['South', 'Down']:
            current_player.y += 1

        elif choice == 'East':
            current_player.x += 1

        elif choice == 'West':
            current_player.x -= 1

        current_player = p2 if current_player == p1 else p1

        # TODO: CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON THE PLAYER'S CHOICE
        #  REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if
        #  the choice the player made was just a movement, so only updating player's position is enough to change the
        #  location to the next appropriate location
        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....
