classes = {1: "Mage", 2: "Warrior", 3: "Rogue"}

class Mage():
    def __init__(self):
        self.name = "Mage"
        self.hp = 50
        self.attack = 15

class Warrior():
    def __init__(self):
        self.name = "Warrior"
        self.hp = 120
        self.attack = 6

class Rogue():
    def __init__(self):
        self.name = "Rogue"
        self.hp = 100
        self.attack = 10


class PlayerProfile():
    def __init__(self, profile_id:str):
        self.profile_id = profile_id
        self.name = None
        self.level = 1
        self.char_class = None
        self.achievements = []
        self.quest_history = []
        self.inventory = []

    def to_dict(self):
        return {
            "profile_id": self.profile_id,
            "name": self.name,
            "level": self.level,
            "char_class": self.char_class,
            "achievements": self.achievements,
            "quest_history": self.quest_history,
            "inventory": self.inventory
        }

    def from_dict(self, data: dict):
        self.profile_id = data.get("profile_id", self.profile_id)
        self.name = data.get("name", self.name)
        self.level = data.get("level", self.level)
        self.char_class = data.get("char_class", self.char_class)
        self.achievements = data.get("achievements", self.achievements)
        self.quest_history = data.get("quest_history", self.quest_history)
        self.inventory = data.get("inventory", self.inventory)
    
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
                if char_class == 1:
                    self.name = name
                    self.char_class = Warrior()
                elif char_class == 2:
                    self.name = name
                    self.char_class = Mage()
                elif char_class == 3:
                    self.name = name
                    self.char_class = Rogue()
                else:
                    print("Invalid class number. Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number (1-3).")

    def __str__(self):
        return str(self.to_dict())
