# Treasure & Trap mini adventure2

from miniAdventure import MiniAdventure
#from realm import Realm
import random


class Player:
    def __init__(self, name: str):
        self.name = name
        self.row = 0
        self.col = 0
        self.treasure_count = 0
        self.skip_next_turn = False

    def move_to(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def add_treasure(self) -> None:
        self.treasure_count += 1

    def skip_turn(self) -> None:
        self.skip_next_turn = True

    def clear_skip(self) -> None:
        self.skip_next_turn = False


class Trap:
    def __init__(self, owner: Player):
        self.owner = owner

    def activate(self, target: Player) -> None:
        target.skip_turn()


class Cell:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.has_treasure = False
        self.trap = None  # Trap or None
        self.occupant = None  # Player or None

    def is_empty(self) -> bool:
        return not self.has_treasure and self.trap is None and self.occupant is None


class GridMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = [[Cell(r, c) for c in range(width)] for r in range(height)]

    def is_inside(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def get_cell(self, row: int, col: int) -> Cell:
        return self.cells[row][col]

    def place_treasure(self, row: int, col: int) -> None:
        if self.is_inside(row, col):
            self.cells[row][col].has_treasure = True

    def place_treasures_randomly(self, count: int) -> None:
        pass


class GridMapAdapter:
    def __init__(self, adaptee: GridMap):
        self.adaptee = adaptee

    def is_valid(self, row: int, col: int) -> bool:
        pass

    def is_empty(self, row: int, col: int) -> bool:
        pass

    def move_player(self, player: Player, row: int, col: int) -> None:
        pass

    def place_trap(self, row: int, col: int, owner: Player) -> None:
        pass

    def remove_trap(self, row: int, col: int) -> None:
        pass

    def remove_treasure(self, row: int, col: int) -> None:
        pass

    def render(self) -> str:
        pass


class TreasureTrapAdventure(MiniAdventure):
    # Nicol: I am calling makeing an instance of this in adventure.py's second class 
    def __init__(self, id: str):
        super().__init__(id)
        pass

    def start_adventure(self):
        # Nicol: please write all of your loop/player input code here see mobHunt for example
        pass

