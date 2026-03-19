from abc import ABC, abstractmethod
from ItemInventory import Inventory, Item, Rarity_enum, ItemType_enum
from typing_extensions import override

# least 2 are on line 68, 67 they are lists of strings
class Adventurer(ABC):
    def __init__(self, name:str, hp:int, attack:int):
        self.name = name
        self.hp = hp
        self.attack = attack
    
    @abstractmethod
    def attackMonster(self):
        pass

    def to_dict(self):
        # this might matter if we need to save the users attack power or hp if it goes up
        return {"name": self.name}

    
    @staticmethod
    def from_dict(data):
        classes = {"Mage":Mage, "Warrior":Warrior, "Rogue":Rogue}
        if isinstance(data, dict):
            ChildObj = classes[data["name"]]()
        else: 
            ChildObj = classes[data]()

        return ChildObj


class Mage(Adventurer):
    def __init__(self):
        super().__init__("Mage", 50, 15)
    
    def attackMonster(self):
        return "Mage throws fireball"

class Warrior(Adventurer):
    def __init__(self):
        super().__init__("Warrior", 120, 6)

    
    def attackMonster(self):
        return "Warrior swings sword"

class Rogue(Adventurer):
    def __init__(self):
        super().__init__("Rogue", 100, 10)


    def attackMonster(self):
        return "Rogue sneak attacks from the front"

AdventurerClasses = {1: Mage, 2: Warrior, 3: Rogue}

class PlayerProfile():
    def __init__(self, profile_id:str):
        self.profile_id = profile_id
        self.name = None
        self.level = 1
        self.char_class = None
        self.achievements = []
        self.quest_history = []
        self.inventory = Inventory()

    def addItem(self, item: Item):
        print(item)
        print(self.inventory)
        self.inventory.AddItem(item)

    def to_dict(self):
        print("inventory", self.inventory.to_dict())
        return {
            "profile_id": self.profile_id,
            "name": self.name,
            "level": self.level,
            "char_class": self.char_class.to_dict(),
            "achievements": self.achievements,
            "quest_history": self.quest_history,
            "inventory": self.inventory.to_dict() #MAYBE CHANGE USING TO_DICT
        }

    def from_dict(self, data: dict):
        self.profile_id = data.get("profile_id", self.profile_id)
        self.name = data.get("name", self.name)
        self.level = data.get("level", self.level)
        self.achievements = data.get("achievements", self.achievements)
        self.quest_history = data.get("quest_history", self.quest_history)
        print(data.get("inventory"))
        print(self.inventory)
        self.inventory.from_dict(data.get("inventory", self.inventory))
        print(f"RETRIEVE DATA {self.inventory}")
        self.char_class = Adventurer.from_dict(data.get("char_class", self.char_class))
    
    def create_player_cli(self):
        print("\n==============================")
        print("Create Player Profile")
        print("==============================")
        print("\n==============================")
        print("Create Character")
        print("==============================")
        name = input("Enter character name: ").strip()
        print("\n==============================")
        print("Pick class:")
        print("1. Warrior")
        print("2. Mage")
        print("3. Rogue")
        print("==============================")
        while True:
            char_class = input("Enter class number (1-3): ").strip()
            try:
                char_class = int(char_class)
                if char_class in AdventurerClasses.keys():
                    self.name = name
                    self.char_class = AdventurerClasses[char_class]()
                    print(self.char_class.attackMonster())
                    return
                
                else:
                    print("Invalid class number. Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number (1-3).")

    def __str__(self):
        return str(self.to_dict())

class NullPlayerProfile(PlayerProfile):
    @override
    def __init__(self):
        self.name = "(none)"

    def __bool__(self):
        return False
    @override
    def addItem(self, item: Item):
        return None
    @override
    def to_dict(self):
        return {}
    @override
    def from_dict(self, data: dict):
        return None
    @override
    def create_player_cli(self):
        return self
    @override
    def __str__(self):
        return "(none)"
    
    
