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
        self.start_position = start
        self.target_position = target
        self.target_points = target_points


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
    points: int
    b_description: str
    l_description: str
    avail_cmd: list[str]
    items: list[Item]
    visited: bool

    def __init__(self, position: int, points:int, b_description:str, l_description:str, commands:list[str], items:list[Item]) -> None:
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
        self.points = 0
        self.b_description = b_description
        self.l_description = l_description
        self.avail_cmd = commands
        self.items = items
        self.visited = False


    def available_actions(self):
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """

        # NOTE: This is just a suggested method
        # i.e. You may remove/modify/rename this as you like, and complete the
        # function header (e.g. add in parameters, complete the type contract) as needed

        for command in self.avail_cmd:
            print(command)


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - x: Horizontal position of Player
        - y: Vertical Position of Player
        - inventory: List of Items carried by Player
        - victory: win status

    Representation Invariants:
        - x >= 0
        - y >= 0
    """

    x: int
    y: int
    inventory: list[list[Item]]
    victory: bool

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False


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
        self.items = self.load_items(items_data)
        self.locations = self.load_locations(location_data)

        # NOTE: You may choose how to store location and item data; create your own World methods to handle these
        # accordingly. The only requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

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
        for l in locations:
            location = l.split('\n')
            position = int(location[0].strip()[9::])
            points = int(location[1])
            b_desc = location[2]
            l_desc = " ".join(l[3::])

            items = [item for item in self.items if item.start_position == location]

            commands = []
            for i in range(len(self.map)):
                if position in self.map[i]:
                    j = self.map.index(position)

                    if j + 1 < len(self.map[i]) and self.map[i][j+1] != -1:
                        commands.append('East')
                    
                    if j - 1 >= 0 and self.map[i][j-1] != -1:
                        commands.append('West')

                    if i + 1 < len(self.map) and self.map[i + 1][j] != -1:
                        commands.append('South')
                    
                    if i - 1 >= 0 and self.map[i - 1][j] != -1:
                        commands.append('North')

                    if items != []:
                        commands.append('Pick Up')
   

            Location(position, points, b_desc, l_desc, commands, items)



    def load_items(self, items_data: TextIO) -> list[Item]:
        """
        Store Items from items file into a list of Item Objects.
        then returns list
        """

        items = items_data.read().split('\n')

        items_list = []

        for item in items:
            item_data = item.split(' ')
            location = item_data[0]
            target = item_data[1]
            points = item_data[2]
            name = " ".join(item_data[3::])

            items_list.append(Item(name, location, target, points))


    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """

        return self.map[y][x] if self.map[y][x] != -1 else None
