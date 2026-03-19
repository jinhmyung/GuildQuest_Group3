# Treasure & Trap mini adventure2

from miniAdventure import MiniAdventure
from realm import Realm
import random

# Item types and rarities
ITEM_TYPES = ["gold_coin", "sword", "diamond", "ancient_ring", "silver_key", "old_map", "gemstone_shard", "guild_medal"]
RARITIES = ["common", "uncommon", "rare", "legendary"]
ITEM_NAMES = {"gold_coin": "Gold Coin", "sword": "Old Sword", "diamond": "Rough Diamond", "ancient_ring": "Ancient Ring", "silver_key": "Silver Key", "old_map": "Old Map", "gemstone_shard": "Gemstone Shard", "guild_medal": "Guild Medal"}


class Item:
    #Treasure item; can be saved to PlayerProfile.inventory as dict.
    def __init__(self, item_type: str, rarity: str, description: str = ""):
        self.item_type = item_type
        self.rarity = rarity
        self.name = ITEM_NAMES.get(item_type, item_type)
    
        if description:
            self.description = description
        elif item_type == "gold_coin":
            self.description = f"A small gold coin, slightly worn. ({rarity})"
        elif item_type == "sword":
            self.description = f"An old sword with a few nicks in the blade. ({rarity})"
        elif item_type == "diamond":
            self.description = f"A rough diamond that still catches the light. ({rarity})"
        elif item_type == "ancient_ring":
            self.description = f"A bronze ring with faded runes carved on the inside. ({rarity})"
        elif item_type == "silver_key":
            self.description = f"A small silver key with no matching lock in sight. ({rarity})"
        elif item_type == "old_map":
            self.description = f"A creased map that shows a path fading into an unmarked forest. ({rarity})"
        elif item_type == "gemstone_shard":
            self.description = f"A shard chipped from a larger gem. It still sparkles a little. ({rarity})"
        elif item_type == "guild_medal":
            self.description = f'A worn Guild medal given long ago for "services rendered". ({rarity})'
        else:
            self.description = f"{self.name} ({rarity})"
        
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
        # pick random type + rarity for each treasure on the map
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
    #One grid -> can hold treasure, trap, or player.
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.has_treasure = False
        self.treasure_item = None  
        self.trap = None 
        self.occupant = None  

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
    #Wraps GridMap to handle moves, traps, and rendering.
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
    def __init__(self, player1, player2, id: str, realm: Realm):
        super().__init__(id)
        self.profile1 = player1 
        self.profile2 = player2
        self.player1 = None  
        self.player2 = None
        self.grid = None
        self.adapter = None
        self.outcome = "IN_PROGRESS"
        self.turn = 1
        self.realm = realm

    def initialize(self):
        self.grid = GridMap(5, 5)
        self.adapter = GridMapAdapter(self.grid)
        self.player1 = Player(getattr(self.profile1, "name", "P1"))
        self.player2 = Player(getattr(self.profile2, "name", "P2"))
        # P1 at top-left, P2 at bottom-right
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
            print(f"  -> Found: {item.name} ({item.rarity})")
            print(f"     {item.description}")
            # also give the item to the player's Inventory
            try:
                from ItemInventory import Item as InvItem
                profile = self.profile1 if player is self.player1 else self.profile2
                desc = item.description
                suffix = f" ({item.rarity})"
                if desc.endswith(suffix):
                    desc = desc[:-len(suffix)]
                inv_item = InvItem(item.name, item.rarity, description=desc)
                profile.addItem(inv_item)
            except Exception:
                # if inventory system changes or fails, still continue the game
                pass
            self.adapter.remove_treasure(player.row, player.col)
        if cell.trap is not None:
            cell.trap.activate(player)
            self.adapter.remove_trap(player.row, player.col)

    def check_win(self):
        # first to 3 treasures wins
        if self.player1.treasure_count >= 3:
            self.outcome = "P1 wins"
        elif self.player2.treasure_count >= 3:
            self.outcome = "P2 wins"

    def player_turn_cli(self, player):
        label = "P1" if player is self.player1 else "P2"
        print(f"\n{label} ({player.name})'s turn")
        while True:  # re-prompt until valid choice 
            choice = input("1.Move 2.Trap 3.Skip 4.Exit: ").strip()
            if choice == "4":
                self.outcome = "DRAW"
                print("  -> You ended the game early. It's a draw!")
                return
            if choice == "1":
                while True:
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
                        print("  -> Invalid direction. Please enter up, down, left, or right.")
                        continue
                    if not self.adapter.is_valid(new_row, new_col):
                        print("  -> Invalid move (out of map). Try again.")
                        continue
                    if self.grid.get_cell(new_row, new_col).occupant is not None:
                        print("  -> Invalid move (cell occupied). Try again.")
                        continue
                    self.adapter.move_player(player, new_row, new_col)
                    self.apply_cell_effect(player)
                    break
                break
            elif choice == "2":
                while True:
                    try:
                        row = int(input("Row (0-4): ").strip())
                        col = int(input("Col (0-4): ").strip())
                    except ValueError:
                        print("  -> Invalid number. Please enter 0-4 for row and col.")
                        continue
                    if self.adapter.place_trap(row, col):
                        print("Trap placed!")
                        break
                    else:
                        print("  -> Cannot place trap there (player/treasure/trap on cell). Try again.")
                break
            elif choice == "3":
                print("You skip this turn.")
                break
            else:
                print("  -> Invalid choice. Please enter 1, 2, 3, or 4.")

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
        # save profiles so collected items show up in main menu inventory
        try:
            from profileManager import ProfileManager
            pm = ProfileManager()
            pm.save(self.profile1.profile_id, self.profile1)
            pm.save(self.profile2.profile_id, self.profile2)
        except Exception:
            pass
