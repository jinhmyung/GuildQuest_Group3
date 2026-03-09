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
        return self.adaptee.is_inside(row, col)

    def is_empty_for_trap(self, row: int, col: int) -> bool:
        pass

    def move_player(self, player: Player, new_row: int, new_col: int) -> None:
        if not self.is_valid(new_row, new_col):
            return
        old_cell = self.adaptee.get_cell(player.row, player.col)
        old_cell.occupant = None

        new_cell = self.adaptee.get_cell(new_row, new_col)
        new_cell.occupant = player
        player.move_to(new_row, new_col)

    def place_trap(self, row: int, col: int) -> bool:
        pass

    def remove_trap(self, row: int, col: int) -> None:
        pass

    def remove_treasure(self, row: int, col: int) -> None:
        pass

    def render(self, player1: Player, player2: Player) -> str:
        lines = []
        for r in range(self.adaptee.height):
            row_str = ""
            for c in range(self.adaptee.width):
                cell = self.adaptee.get_cell(r, c)
                if cell.occupant == player1:
                    row_str += "1 "
                elif cell.occupant == player2:
                    row_str += "2 "
                elif cell.has_treasure:
                    row_str += "T "
                elif cell.trap:
                    row_str += "X "
                else:
                    row_str += ". "
            lines.append(row_str)
        return "\n".join(lines)


class TreasureTrapAdventure(MiniAdventure):
    def __init__(self, player1, player2, id: str):
        super().__init__(id)
        self.profile1 = player1  # from GuildQuest (name, level, etc)
        self.profile2 = player2
        self.player1 = None  # on map (position, treasure, etc)
        self.player2 = None
        self.grid = None
        self.adapter = None
        self.outcome = "IN_PROGRESS"
        self.turn = 1

    def initialize(self):
        self.grid = GridMap(5, 5)
        self.adapter = GridMapAdapter(self.grid)
        self.player1 = Player(getattr(self.profile1, "name", "P1"))
        self.player2 = Player(getattr(self.profile2, "name", "P2"))
        self.grid.get_cell(0, 0).occupant = self.player1
        self.player1.move_to(0, 0)
        self.grid.get_cell(4, 4).occupant = self.player2
        self.player2.move_to(4, 4)

    def apply_cell_effect(self, player):
        pass  # TODO

    def check_win(self):
        pass  # TODO

    def player_turn_cli(self, player):
        print(f"\n{player.name}'s turn")
        choice = input("1.Move 2.Trap 3.Skip: ").strip()
        if choice == "1":
            direction = input("up/down/left/right? ").strip().lower()
            if direction == "up":
                new_row, new_col = player.row - 1, player.col
            elif direction == "down":
                new_row, new_col = player.row + 1, player.col
            elif direction == "left":
                new_row, new_col = player.row, player.col - 1
            elif direction == "right":
                new_row, new_col = player.row, player.col + 1
            else:
                print("Invalid")
                return
            if self.adapter.is_valid(new_row, new_col) and self.grid.get_cell(new_row, new_col).occupant is None:
                self.adapter.move_player(player, new_row, new_col)
                self.apply_cell_effect(player)
        elif choice == "2":
            pass  # TODO

    def handle_input(self, player_input: str):
        pass

    def update(self):
        pass

    def get_state(self):
        return self.outcome

    def is_finished(self):
        return self.outcome != "IN_PROGRESS"

    def get_result(self):
        return self.outcome

    def reset(self):
        # TODO
        self.outcome = "IN_PROGRESS"

    def start_adventure(self):
        self.initialize()
        print("\n==============================")
        print("Treasure & Trap")
        print("==============================")
        print("1, 2 = players  T = treasure  X = trap  . = empty")
        print("First to 3 treasures wins!")
        print("==============================")

        while not self.is_finished():
            # show map and scores
            print(self.adapter.render(self.player1, self.player2))
            print(f"P1: {self.player1.treasure_count}  P2: {self.player2.treasure_count}")

            if self.turn == 1:
                self.player_turn_cli(self.player1)
                self.turn = 2
            else:
                self.player_turn_cli(self.player2)
                self.turn = 1

            self.check_win()

        print(f"Game over! {self.outcome}")

