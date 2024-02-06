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
from game_data import World, Item, Location, Player, Pen, Hint, Reference, ID, Treasure

MOVES_PER_TURN = 5
BACK_STORY = """Your friend and you have got an important exam coming up, and you've been studying for weeks.
Last night was a particularly late night on campus. To focus, rather than staying in one place, the both of you studied in varied
places throughout the night. Unfortunately, the both of you ended up losing your T-card as the night progressed and you're nervous because
they might not let you two into the exam room! Also, you two have also lost your lucky pens. To make things worse, the cheat sheet you made 
overnight has gone missing as well. All of this stuff must be around campus somewhere. Can you two find it before the exam begins?
"""
RULES = ("=" * 120) + '\n' + "RULES".center(120) + """
-> To clear the game, you two have to find your T-card, lucky pen, and cheat sheet and deposit it at the exam centre.
-> You accumulate and spend points by visiting locations or finding items.
-> The person with the higher points wins at the end.
-> You have to collect the items and deposit them at the Exam Center\n""" + ("=" * 120)


def player_pickup(current_player: Player, item:Item, name: str, location: Location) -> None:

    if isinstance(item, Pen):

        if current_player.hasPen:
            print("You already have a Pen!")
        else:
            print("You collected the", name)
            current_player.hasPen = True
            item.pick_up(current_player)
            location.contained_items.remove(item)

    elif isinstance(item, Reference):

        if current_player.hasReference:
            print("You already have a Reference Item!")
        else:
            print("You collected the", name)
            item.pick_up(current_player)
            current_player.hasReference = True
            location.contained_items.remove(item)

    elif isinstance(item, Hint):

        print("You pick up the Treasure Map, and it reads the following:\n")
        item.read()
        print()

    elif isinstance(item, ID):
        if current_player.hasID:
            print("You already have your ID")
        else:
            print("You collected the", name)
            item.pick_up(current_player)
            current_player.hasID = True
            location.contained_items.remove(item)

    else:
        print("You collected the", name)
        item.pick_up(current_player)
        location.contained_items.remove(item)


def player_look(current_player: Player, location: Location) -> None:
    """The Look move for the player
    """

    print("After a light gloss you found ", end="")
    if location.contained_items != []:
        items = [i.name.capitalize()
                 for i in location.contained_items if not isinstance(i, Treasure)]
        print(", ".join(items))

        pickup = input("What would you like to pickup (type none to not pickup):\t").capitalize().strip()

        if pickup not in items:
            print("You picked up nothing")

        for item in location.contained_items:
            name = item.name.capitalize()

            if name == pickup:
                player_pickup(current_player, item, name, location)

    else:
        print("Nothing\n")


def player_deposit(current_player: Player, w: World) -> None:
    """The Deposit inventory move for the current player
    """
    for item in current_player.inventory:

        if not item.deposited and item.target_position == w.get_location(current_player.x,
                                                                         current_player.y).position:
            item.deposit(current_player, w)
            print("Deposited", item.name)


def player_take_test(current_player: Player, w: World) -> None:
    if current_player.target_x != current_player.x or current_player.target_y != current_player.y:
        print("Need to go to Test Center to take the Test")

    elif not (current_player.hasPen and current_player.hasReference and current_player.hasPen):
        print("You are missing some required material")

    else:
        print("Auto-depositing test materials")
        for item in current_player.inventory:

            if not item.deposited and item.target_position == w.get_location(current_player.x,
                                                                                current_player.y).position:
                item.deposit(current_player, w)

        print(current_player.name, "Finished the game!\n")
        current_player.victory = True


def player_search_treasure(current_player, location) -> None:
    print("Lost Energy while searching, score:\t-100")
    current_player.score -= 100
    items = [i for i in location.contained_items if isinstance(i, Treasure)]

    if items != []:

        print("You found Treasure!!")
        item = items[0]
        print("You collected", "✨", item.name.capitalize(), "✨")
        item.pick_up(current_player)
        location.contained_items.remove(item)

    else:
        print("You found no Hidden Treasure")


def player_inventory(current_player) -> None:
    if current_player.hasID:
        print(current_player.name, "has their ID\n")

    if current_player.hasPen:
        print(current_player.name, 'has a Pen\n')

    if current_player.hasReference:
        print(current_player.name, 'has a Reference\n')

    if current_player.inventory == []:
        print("You have no Items")

    for item in current_player.inventory:
        print(item.name)


def play_game() -> None:
    """ Play the Text Adventure Game
    """
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))

    target = w.get_position(00)

    p1 = Player("Player 1", 0, 2, target[0], target[1])
    # set starting location of player; you may change the x, y coordinates here as appropriate
    p2 = Player("Player 2", 0, 4, target[0], target[1])

    menu = ["Look", "Search treasure", "Inventory", "Score", "Quit", "Rules", "Map",
            "Read", "Write", "Deposit", "Take test"]

    current_player = p1
    moves_this_turn = 0

    print('\n\n\n' + BACK_STORY)
    print(RULES, '\n\n')

    while not p1.victory or not p2.victory:

        if p1.victory:
            current_player = p2
        elif p2.victory:
            current_player = p1

        if moves_this_turn == 0:
            print('#' * 60)
            print((current_player.name + "'s Turn").center(60))
            print('#' * 60)

        location = w.get_location(current_player.x, current_player.y)

        if location.visited:
            print(location.b_description)
        else:
            print(location.l_description)
            location.visited = True

        print("\nWhat do you do? \n")
        print("[menu]")
        for action in location.available_actions():
            print(action.title())

        choice = input("\nEnter action:\t").capitalize().strip()

        while choice in menu + ['[menu]'] and choice not in location.available_actions():

            if choice == "[menu]":
                print("Menu Options: \n")
                for option in menu:
                    print(option)
                print()

            elif choice == 'Look':
                player_look(current_player, location)

            elif choice == "Deposit":
                player_deposit(current_player, w)
                break

            elif choice == "Take test":
                player_take_test(current_player, w)
                if current_player.victory:
                    moves_this_turn = MOVES_PER_TURN + 1
                break

            elif choice == "Search treasure":
                player_search_treasure(current_player, location)
                break

            elif choice == 'Inventory':
                player_inventory(current_player)

            elif choice == "Score":
                print(current_player.name.upper() + ":", current_player.score)

            elif choice == 'Read':

                if current_player.hasReference:
                    ref = [i for i in current_player.inventory if isinstance(i, Reference)][0]
                    ref.study(current_player)

                else:
                    print("You don't have a Reference to Study from!")

                break

            elif choice == 'Write':

                if current_player.hasPen:
                    pen = [i for i in current_player.inventory if isinstance(i, Pen)][0]
                    pen.practise_handwriting(current_player)

                else:
                    print("You don't have a pen to practise!")

                break

            elif choice == "Quit":
                print(p1.name.upper() + ":", p1.score)
                print(p2.name.upper() + ":", p2.score)

                if p1.score > p2.score and p1.victory:
                    print(p1.name, "Won")
                elif p2.score < p1.score and p2.victory:
                    print(p2.name, "Won")

                print("GAME OVER!!")
                exit()

            elif choice == "Map":
                w.draw_map(p1, p2)

            elif choice == "Rules":
                print(RULES)

            else:
                print('NOT A VALID ACTION! xP')

            print(location.b_description)

            for action in location.available_actions():
                print(action.title())

            choice = input("\nEnter action:\t").capitalize().strip()

        if choice == "Go north":
            dy = -1
            location = w.get_location(current_player.x, current_player.y + dy)
            while location is None or location.position % 10 != 0:
                dy -= 1
                location = w.get_location(current_player.x, current_player.y + dy)

            current_player.y += dy

        elif choice == "Go south":
            dy = 1
            location = w.get_location(current_player.x, current_player.y + dy)
            while location is None or location.position % 10 != 0:
                dy += 1
                location = w.get_location(current_player.x, current_player.y + dy)

            current_player.y += dy

        elif choice == 'Go up':
            current_player.y -= 1

        elif choice == 'Go down':
            current_player.y += 1

        elif choice == 'Go east':
            current_player.x += 1

        elif choice == 'Go west':
            current_player.x -= 1

        moves_this_turn += 1

        if moves_this_turn >= MOVES_PER_TURN:

            if current_player == p1 and not p2.victory:
                current_player = p2

            elif current_player == p2 and not p1.victory:
                current_player = p1

            moves_this_turn = 0

    print(p1.name.upper() + ":", int(p1.score))
    print(p2.name.upper() + ":", int(p2.score))

    if p1.score > p2.score and p1.victory:
        print(p1.name, "Won")
    elif p2.score < p1.score and p2.victory:
        print(p2.name, "Won")


if __name__ == "__main__":

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })

    play_game()
