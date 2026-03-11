# Treasure & Trap mini adventure2

from miniAdventure import MiniAdventure
#from realm import Realm
import random

# Item types and rarities (stored in PlayerProfile.inventory as dicts)
ITEM_TYPES = ["gold_coin", "sword", "bomb"]
RARITIES = ["common", "uncommon", "rare", "legendary"]
ITEM_NAMES = {"gold_coin": "Gold Coin", "sword": "Sword", "bomb": "Bomb"}


class Item:
    """Treasure item: gold_coin, sword, or bomb. Stored in profile.inventory as to_dict()."""
    def __init__(self, item_type: str, rarity: str, description: str = ""):
        self.item_type = item_type
        self.rarity = rarity
        self.name = ITEM_NAMES.get(item_type, item_type)
        self.description = description or f"{self.name} ({rarity})"

    def to_dict(self):
        return {
            "name": self.name,
            "item_type": self.item_type,
            "rarity": self.rarity,
            "description": self.description,
        }

    @staticmethod
    def from_dict(d: dict) -> "Item":
        return Item(
            d.get("item_type", "gold_coin"),
            d.get("rarity", "common"),
            d.get("description", ""),
        )

    @staticmethod
    def random_item() -> "Item":
        t = random.choice(ITEM_TYPES)
        r = random.choice(RARITIES)
        return Item(t, r)


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
        self.treasure_item = None  # Item or None (what you get when you step on T)
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

    def place_treasure(self, row: int, col: int, item: Item = None) -> None:
        if self.is_inside(row, col):
            cell = self.cells[row][col]
            cell.has_treasure = True
            cell.treasure_item = item

    def place_treasures_randomly(self, count: int) -> None:
        empty = [(r, c) for r in range(self.height) for c in range(self.width)
                 if self.get_cell(r, c).is_empty()]
        for (r, c) in random.sample(empty, min(count, len(empty))):
            self.place_treasure(r, c, Item.random_item())


class GridMapAdapter:
    def __init__(self, adaptee: GridMap):
        self.adaptee = adaptee

    def is_valid(self, row: int, col: int) -> bool:
        return self.adaptee.is_inside(row, col)

    def is_empty_for_trap(self, row: int, col: int) -> bool:
        if not self.is_valid(row, col):
            return False
        cell = self.adaptee.get_cell(row, col)
        return cell.occupant is None and not cell.has_treasure and cell.trap is None

    def move_player(self, player: Player, new_row: int, new_col: int) -> None:
        if not self.is_valid(new_row, new_col):
            return
        old_cell = self.adaptee.get_cell(player.row, player.col)
        old_cell.occupant = None

        new_cell = self.adaptee.get_cell(new_row, new_col)
        new_cell.occupant = player
        player.move_to(new_row, new_col)

    def place_trap(self, row: int, col: int) -> bool:
        if not self.is_empty_for_trap(row, col):
            return False
        self.adaptee.get_cell(row, col).trap = Trap()
        return True

    def remove_trap(self, row: int, col: int) -> None:
        if not self.is_valid(row, col):
            return
        cell = self.adaptee.get_cell(row, col)
        cell.trap = None

    def remove_treasure(self, row: int, col: int) -> None:
        if not self.is_valid(row, col):
            return
        cell = self.adaptee.get_cell(row, col)
        cell.has_treasure = False
        cell.treasure_item = None

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
        self.grid.place_treasures_randomly(5)
        self.turn = 1

    def apply_cell_effect(self, player):
        cell = self.grid.get_cell(player.row, player.col)
        if cell.has_treasure and cell.treasure_item is not None:
            player.add_treasure()
            item = cell.treasure_item
            profile = self.profile1 if player is self.player1 else self.profile2
            profile.inventory.append(item.to_dict())
            print(f"  -> You got: {item.name} ({item.rarity})! Added to your inventory.")
            self.adapter.remove_treasure(player.row, player.col)
        if cell.trap is not None:
            cell.trap.activate(player)
            self.adapter.remove_trap(player.row, player.col)

    def check_win(self):
        if self.player1.treasure_count >= 3:
            self.outcome = "P1 wins"
        elif self.player2.treasure_count >= 3:
            self.outcome = "P2 wins"

    def player_turn_cli(self, player):
        label = "P1" if player is self.player1 else "P2"
        print(f"\n{label} ({player.name})'s turn")
        choice = input("1.Move 2.Trap 3.Skip 4.Exit: ").strip()
        if choice == "4":
            self.outcome = "DRAW"
            print("  -> You ended the game early. It's a draw!")
            return
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
            try:
                row = int(input("Row (0-4): ").strip())
                col = int(input("Col (0-4): ").strip())
                if self.adapter.place_trap(row, col):
                    print("Trap placed!")
                else:
                    print("Cannot place trap there (occupied or has treasure/trap).")
            except ValueError:
                print("Invalid number.")
        elif choice == "3":
            print("You skip this turn.")

    def handle_input(self, player_input: str):
        if player_input == "1":
            self.player_turn_cli(self.player1)
        elif player_input == "2":
            self.player_turn_cli(self.player2)

    def update(self):
        if self.turn == 1:
            self.player_turn_cli(self.player1)
            self.turn = 2
        else:
            self.player_turn_cli(self.player2)
            self.turn = 1

    def get_state(self):
        return self.outcome

    def is_finished(self):
        return self.outcome != "IN_PROGRESS"

    def get_result(self):
        return self.outcome

    def reset(self):
        self.grid = GridMap(5, 5)
        self.adapter = GridMapAdapter(self.grid)
        self.player1 = Player(getattr(self.profile1, "name", "P1"))
        self.player2 = Player(getattr(self.profile2, "name", "P2"))
        self.grid.get_cell(0, 0).occupant = self.player1
        self.player1.move_to(0, 0)
        self.grid.get_cell(4, 4).occupant = self.player2
        self.player2.move_to(4, 4)
        self.grid.place_treasures_randomly(5)
        self.outcome = "IN_PROGRESS"
        self.turn = 1

    def start_adventure(self):
        self.initialize()
        print("\n==============================")
        print("Treasure & Trap")
        print("==============================")
        print("Two players take turns on a 5x5 grid. Each turn you can:")
        print("  1) Move one step (up/down/left/right)")
        print("  2) Place a trap on an empty cell")
        print("  3) Skip your turn")
        print("  4) Exit - return to main menu, game counts as draw (平局)")
        print("Treasures (T) are items: Gold Coin, Sword, or Bomb (random rarity).")
        print("They go to your inventory. If you step on a trap (X), you skip your next turn!")
        print("First to 3 treasures wins! View your inventory from the main menu after the game.")
        print("==============================")
        print("Map: 1, 2 = players  T = treasure  X = trap  . = empty")
        print("==============================")

        while not self.is_finished():
            print(self.adapter.render(self.player1, self.player2))
            print(f"P1: {self.player1.treasure_count}  P2: {self.player2.treasure_count}")

            if self.turn == 1:
                if self.player1.skip_next_turn:
                    print(f"\n{self.player1.name} skips this turn (trap!).")
                    self.player1.clear_skip()
                    self.turn = 2
                else:
                    self.player_turn_cli(self.player1)
                    self.turn = 2
            else:
                if self.player2.skip_next_turn:
                    print(f"\n{self.player2.name} skips this turn (trap!).")
                    self.player2.clear_skip()
                    self.turn = 1
                else:
                    self.player_turn_cli(self.player2)
                    self.turn = 1

            self.check_win()

        result_msg = "DRAW" if self.outcome == "DRAW" else self.outcome
        print(f"Game over! {result_msg}")
        # Save both profiles so inventory is persisted (viewable from main menu)
        try:
            from profileManager import ProfileManager
            pm = ProfileManager()
            pm.save(self.profile1.profile_id, self.profile1)
            pm.save(self.profile2.profile_id, self.profile2)
        except Exception:
            pass

