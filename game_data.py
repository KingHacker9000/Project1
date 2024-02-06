"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Optional, TextIO
import math, json, random

class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: Name of Item
        - start_position: Starting Position of Item
        - target_position: Location for item to be deposited
        - target_points: Points for Depositing Item

    Representation Invariants:
        - name != ""
        - target_points > 0
    """
    name: str
    start_position: int
    target_position: int
    target_points: int
    deposited: bool

    def __init__(self, name: str, start: int, target: int, target_points: int) -> None:
        """Initialize a new item.
        """

        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.start_position = int(start)
        self.target_position = int(target)
        self.target_points = int(target_points)
        self.deposited = False

    def pick_up(self, player):
        player.inventory.append(self)
        if self.start_position == self.target_position:
            player.score += self.target_points
            self.deposited = True

    def deposit(self, player, world):
        if not self.deposited and self.target_position == world.get_location(player.x, player.y).position:
            player.score += int(self.target_points)
            self.deposited = True

    def __repr__(self) -> str:
        return self.name + " => " + str(self.start_position)


class Reference(Item):

    def study(self, player):

        if random.randint(1,10) < 2:
            print("There was an Error in the Reference Sheet! D:")
            print('Score\t-', self.target_points)
            player.score -= self.target_points

        else:
            print("Hooray! You studied and feel more prepared for the Test :D")
            print('Score\t+', self.target_points//2)
            player.score += self.target_points // 2


class Pen(Item):

    def practise_handwriting(self, player):
        print("Hooray! You studied and feel more prepared for the Test :D")
        print('Score\t+', math.fabs(self.target_points) // 5)
        player.score += math.fabs(self.target_points) // 5


class ID(Item):
    pass

class Treasure(Item):

    def pick_up(self, player):
        player.inventory.append(self)
        player.score += self.target_points
        self.deposited = True

class Hint(Item):

    def __init__(self, name: str, start: int, target: int, target_points: int, hint: str) -> None:
        """Initialize a new item.
        """

        self.name = name
        self.start_position = int(start)
        self.target_position = int(target)
        self.target_points = int(target_points)
        self.deposited = False
        self.hint = hint

    def read(self):
        print(self.hint)

    def __repr__(self) -> str:
        return self.name + " = " + self.hint + " => " + str(self.start_position) + str(type(self))

class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - position: The position of the location in the world map
        - points: Number of points gained by visiting the location
        - b_description: A brief description that is displayed from the second entry to the location
        - l_description: A long description that is displayed on the first entry to the location
        - avail_cmd: A list of available commands from the current location
        - items: Items availaible at the current location
        - visited: Whether the location has been visited before or not

    Representation Invariants:
        - self.b_description != ''
        - self.l_description != ''
        - self.avail_cmd != []
        - self.position >= 0
    """
    position: int
    name: str
    b_description: str
    l_description: str
    avail_cmd: list[str]
    contained_items: list[Item]
    visited: bool

    def __init__(self, position: int, name:str, b_description:str, l_description:str, commands:list[str], items:list[Item] = []) -> None:
        """Initialize a new location.

        """

        # NOTES:
        # Data that could be associated with each Location object:
        # a position in the world map,
        # a brief description,
        # a long description,
        # a list of available commands/directions to move,
        # items that are available in the location,
        # and whether the location has been visited before.
        # Store these as you see fit, using appropriate data types.
        #
        # This is just a suggested starter class for Location.
        # You may change/add parameters and the data available for each Location object as you see fit.
        #
        # The only thing you must NOT change is the name of this class: Location.
        # All locations in your game MUST be represented as an instance of this class.

        self.position = position
        self.name = name
        self.b_description = b_description
        self.l_description = l_description
        self.avail_cmd = commands
        self.contained_items = items
        self.visited = False


    def add_items(self, items: list[Item]):
        self.contained_items.extend(items)

    def available_actions(self):
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """

        return self.avail_cmd


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - x: Horizontal position of Player
        - y: Vertical Position of Player
        - inventory: List of Items carried by Player
        - victory: win status
        - score: points awarded to the player

    Representation Invariants:
        - x >= 0
        - y >= 0
    """

    name: str
    x: int
    y: int
    inventory: list[Item]
    victory: bool
    score: int
    hasPen: bool
    hasID: bool
    hasReference: bool
    target_x: int
    target_y: int

    def __init__(self, name:str, x: int, y: int, target_x: int, target_y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.name = name
        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False
        self.score = 0
        self.hasPen = False
        self.hasID = False
        self.hasReference = False
        self.target_x = target_x
        self.target_y = target_y


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - # TODO add more instance attributes as needed; do NOT remove the map attribute

    Representation Invariants:
        - # TODO
    """

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)
        self.locations = self.load_locations(location_data)
        self.items = self.load_items(items_data)

        for l in self.locations:
            items = [item for item in self.items if item.start_position == l.position]
            l.contained_items = items
    

    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """
        map = []
        s = map_data.read() 
        for line in s.split('\n'):
            if line == "":
                continue
            row = []
            for location_id in line.split(" "):
                row.append(int(location_id))

            map.append(row)

        return map

    def load_locations(self, locations_data: TextIO) -> list[Location]:
        """
        Store locations from locations file into a list of Location Objects.
        then returns list
        """

        locations = locations_data.read().split('END\n\n')
        
        locations_list = []

        for l in locations:
            location = l.split('\n')
            position = int(location[0].strip()[9::])
            name = location[1]
            b_desc = location[2]
            l_desc = "".join(location[3::]).strip()

            commands = []

            if position > -1:
                for i in range(len(self.map)):
                    if position in self.map[i]:
                        j = self.map[i].index(position)

                        if j + 1 < len(self.map[i]) and self.map[i][j+1] > -1 and self.map[i][j] % 10 == 0 and self.map[i][j+1] % 10 == 0:
                            commands.append('Go east')
                        
                        if j - 1 >= 0 and self.map[i][j-1] > -1 and self.map[i][j] % 10 == 0 and self.map[i][j-1] % 10 == 0:
                            commands.append('Go west')

                        if i - 1 >= 0 and self.map[i - 1][j] > -1:
                            if math.fabs(self.map[i-1][j] - self.map[i][j]) < 10:
                                commands.append('Go up')

                            elif self.map[i][j] % 10 == 0:
                                n = i-1
                                while n > 0 and self.map[n][j] != -1:
                                    if self.map[n][j] % 10 == 0:
                                        commands.append('Go north')
                                        break
                                    n -= 1

                        if i + 1 < len(self.map) and self.map[i + 1][j] > -1:
                            if math.fabs(self.map[i][j] - self.map[i+1][j]) < 10:
                                commands.append('Go down')

                            elif self.map[i][j] % 10 == 0:
                                n = i + 1
                                while n < len(self.map) and self.map[n][j] != -1:
                                    if self.map[n][j] % 10 == 0:
                                        commands.append('Go south')
                                        break
                                    n += 1
   

            locations_list.append(Location(position, name, b_desc, l_desc, commands))

        return locations_list


    def load_items(self, items_data: TextIO) -> list[Item]:
        """
        Store Items from items file into a list of Item Objects.
        then returns list
        """

        items = items_data.read().split('\n')

        items_list = []

        for item in items:
            item_data = item.split(' ')
            location = int(item_data[0])
            target = item_data[1]
            points = item_data[2]
            item_type = item_data[3] 
            name = " ".join(item_data[4::])

            if item_type == 'Reference':
                items_list.append(Reference(name, location, target, points))
            
            elif item_type == 'Pen':
                items_list.append(Pen(name, location, target, points))

            elif location == -1:
                x = random.randint(0, len(self.map[0])-1)
                y = random.randint(0, len(self.map)-1)
                while self.get_location(x, y) is None:
                    x = random.randint(0, len(self.map[0])-1)
                    y = random.randint(0, len(self.map)-1)

                location = self.get_location(x, y).position

                hintx = random.randint(0, len(self.map[0])-1)
                hinty = random.randint(0, len(self.map)-1)
                while self.get_location(hintx, hinty) is None:
                    hintx = random.randint(0, len(self.map[0])-1)
                    hinty = random.randint(0, len(self.map)-1)

                hintLocation = self.get_location(hintx, hinty).position
                items_list.append(Hint("Treasure Map", hintLocation, hintLocation, 0, f"Hear ye, Seekers bold and keen, a lost prize at an unknown scene! To reclaim the treasures I hide, follow the path I provide. Higher or Forward, my message is cryptic, but you'll find great pleasure looking {int(math.fabs(hinty - y)) if hinty - y != 0 else 'none'} {'away from' if hinty - y <= 0 else 'towards'} the arctic. But do not forget {int(math.fabs(hintx - x)) if hintx - x != 0 else 'none'} {'away from' if hintx - x >= 0 else 'towards'} the sunrise, is where my treasure hidden lies"))
                items_list.append(Treasure(name, location, target, points))

            else:
                items_list.append(Item(name, location, target, points))

        # print(items_list)
        return items_list


    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """

        if self.map[y][x] <= -1 :
            return None

        for location in self.locations:
            if location.position == self.map[y][x]:
                return location
            
        
    def get_position(self, position: int) -> Optional[tuple[int]]:
        """Return x and y values for a position"""

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):

                if self.map[y][x] == position:
                    return (x, y)

        return None

    def draw_map(self, p1: Player = None, p2: Player = None):

        buildings = []

        for x in range(len(self.map[0])):

            column = []
            building_height = None
            prev_location = None
            for y in range(len(self.map)):

                if self.map[y][x] == -1:

                    if building_height is not None and building_height != 0:
                        column.append(building_height)
                    building_height = 0
                    column.append(building_height)

                elif self.map[y][x] > -1:
                    location = self.get_location(x, y)

                    p = location.position

                    if prev_location is not None and math.fabs(p - prev_location) < 10:
                        building_height += 1

                    else:

                        if building_height is not None and building_height != 0:
                            column.append(building_height)

                        building_height = 1

                    prev_location = p

            if building_height is not None and building_height != 0:
                column.append(building_height)

            buildings.append(column)


        map = ""
        print(buildings)

        yPos = sum([max([buildings[i][j] for i in range(len(buildings))]) for j in range(len(buildings[0]))]) -1

        for i in range(len(buildings[0])-1, -1, -1):

            xPos = 0
            tallest = max([buildings[y][i] for y in range(len(buildings))])

            block = []
            names = ''

            for j in range(len(buildings)):

                yBase = yPos

                for x in range(buildings[j][i]):

                    y = x * 3
                    print(yPos, xPos)

                    s = "▢"
                    if yPos == p1.y and xPos == p1.x:
                        s = "A"
                    elif yPos == p2.y and xPos == p2.x:
                        s = "B"

                    if len(block) > y+2:
                        block[y+2] +=   "|           |\t"
                        
                        block[y+1] += f"| ▢ ▢ {s} ▢ ▢ |\t"
                        block[y] += "|___________|\t"
                    else:
                        block.append("|___________|\t")
                        block.append(f"| ▢ ▢ {s} ▢ ▢ |\t")
                        block.append("|           |\t")
                    yPos -= 1

                yPos = yBase

                if buildings[j][i] > 0:
                    if len(block) > y+3:
                        block[y+3] += " ___________ \t"  
                    else:
                        block.append(" ___________ \t")
                    y+=3

                while y < tallest:
                    if len(block) > y+1:
                        block[y+1] += " "*12 + '\t'
                    else:
                        block.append(" "*12 + '\t')
                    y += 1

                if self.map[yPos][xPos] % 10 == 0:
                    names += self.get_location(xPos, yPos).name[:13:].center(13) + "   "
                    

                xPos += 1

            map = "\n".join(block[::-1]) + f'\n{names}' + '\n\n' + map
            print(tallest)
            yPos -= tallest

        print(map)


    def __repr__(self) -> str:
        s = 'MAP:\n'

        import json
        s += json.dumps(self.map, indent=4)

        s += '\nItems:\n'
        for item in self.items:
            s += " | ".join([item.name, item.start_position, item.target_position]) + "\n"

        s += '\nLocations:\n'
        for location in self.locations:
            s += " | ".join([str(location.position), location.l_description]) + '\n'

        return s

if __name__ == "__main__":

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })