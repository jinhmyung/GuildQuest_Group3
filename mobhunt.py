from miniAdventure import MiniAdventure
from playerProfile import PlayerProfile
from ItemInventory import Item
from realm import Realm
import random

#CREATE SOME RANDOM MONSTER BASED ON REALM DIFFICULTY
class MonsterFactory:

    class Monster:
        def __init__(self, name: str, hp: int, attack: int, drop: Item):
            self.name = name
            self.hp = hp
            self.attack = attack
            self.drop = drop



    @staticmethod
    def create_monster(realm_difficulty: str):
        if realm_difficulty == "easy":
            return MonsterFactory._random_easy_monster()

        elif realm_difficulty == "medium":
            return MonsterFactory._random_medium_monster()

        elif realm_difficulty == "hard":
            return MonsterFactory._random_hard_monster()
        elif realm_difficulty == "extreme":
            return MonsterFactory._random_extreme_monster()
        else:
            raise ValueError(f"Unknown realm difficulty: {realm_difficulty}")


    @staticmethod
    def _random_easy_monster():
        return random.choice([
            MonsterFactory.Monster("Goblin", 100, 4, Item("Green", "uncommon", "Tools", "IDK")),
            MonsterFactory.Monster("Orc", 150, 6, Item("Teeth", "uncommon", "Tools", "Sharp teeth"))
        ])


    @staticmethod
    def _random_medium_monster():
        return random.choice([
            MonsterFactory.Monster("Debt Collector", 100, 20, Item("Checkbook", "common", "Tools", "Money")),
            MonsterFactory.Monster("Troll", 200, 8, Item("Club", "common", "Tools", "Big club"))
        ])


    @staticmethod
    def _random_hard_monster():
        return random.choice([
            MonsterFactory.Monster("Dragon", 300, 15, Item("Head", "rare", "Tools", "Dragon head")),
            MonsterFactory.Monster("Demon Lord", 500, 10, Item("Cool Sword", "rare", "Tools", "Cool looking sword"))
        ])
    
    @staticmethod
    def _random_extreme_monster():
        return random.choice([
            MonsterFactory.Monster("Gojo Satoru", 1000, 200, Item("Eyes", "epic", "Tools", "Eyes")),
            MonsterFactory.Monster("Trash can", 10000000000000000000, 1, Item("Trash Can", "epic", "Tools", "Trashhh"))
        ])

class MobHunt(MiniAdventure):

    def __init__(self, player1: PlayerProfile, player2: PlayerProfile, id: str, realm: Realm):
        super().__init__(id)
        print(realm)
        self.state = "ongoing"
        self.turn = 1
        self.result = None
        self.player1 = player1
        self.player2 = player2
        self.monster = MonsterFactory.create_monster(realm.difficulty)
        self.id = id
        self.realm = realm
    
    #CAN USE TO SET REALM SHOULD REPLACE INIT WITH THIS MAYBE??? BUT INIT DOES THE SAME THING
    def initialize(self, player1: PlayerProfile, player2: PlayerProfile):
        self.player1 = player1
        self.player2 = player2


    #NEVER USED
    def update(self):
        return
    
    #NEVER USED
    def get_state(self):
        return self.state

    #CHECK IF THE GAME IS FINISHED
    def is_finished(self):
        if self.monster.hp <= 0:
            self.state = "finished"
            self.result = "success"
            return True
        elif self.player1.char_class.hp <= 0 and self.player2.char_class.hp <= 0:
            self.state = "finished"
            self.result = "failure"
            return True
        else:
            return False

    #NEVER USED
    def get_result(self):
        return self.result

    #NEVER USED
    def reset(self):
        self.state = "not started"
        self.result = None

    #RANDOMLY SELECT AN ATTACK -- SAME AS PLAYER INPUT
    def monsterRNG(self, player: PlayerProfile):
        random_number = random.randint(1, 3)
        print(random_number)
        if random_number == 1:
            hit_chance = random.randint(1, 100)
            if hit_chance <= 90:
                damage = self.monster.attack
                self.monster.hp -= damage
                player.char_class.hp -= damage
                print(f"{self.monster.name} attacks {player.name} for {damage} damage!")
            else:
                print(f"{self.monster.name} missed the attack on {player.name}!")
        elif random_number == 2:
            hit_chance = random.randint(1, 100)
            if hit_chance <= 50:
                damage = self.monster.attack * 1.5
                player.char_class.hp -= damage
                print(f"{self.monster.name} uses a heavy attack on {player.name} for {damage} damage!")
            else:
                print(f"{self.monster.name} missed the heavy attack on {player.name}!")
        elif random_number == 3:
            hit_chance = random.randint(1, 100)
            if hit_chance <= 10:
                damage = self.monster.attack * 2
                player.char_class.hp -= damage
                print(f"{self.monster.name} uses a special attack on {player.name} for {damage} damage!")
            else:
                print(f"{self.monster.name} missed the special attack on {player.name}!")
    
    #CALLS monsterRNG FUNCTION TO RANDOMLY USE AN ATTACK
    def monster_turn_cli(self):
        print(f"\n{self.monster.name}'s turn")
        target = random.choice([self.player1, self.player2])
        while target.char_class.hp <= 0:
            target = random.choice([self.player1, self.player2])
        self.monsterRNG(target)


    # changed this method name since it should probably be the same for both miniAdventures
    def start_adventure(self):
        while True:
            self.status_bar_cli()
            if self.is_finished():
                print(f"Adventure finished! Result: {self.get_result()}")
                return
            if self.turn == 1:
                self.player_turn_cli(self.player1)
                self.turn = 2
            elif self.turn == 2:
                self.player_turn_cli(self.player2)
                self.turn = 3
            elif self.turn == 3:
                self.monster_turn_cli()
                self.turn = 1
    #HANDLES
    #PLAYER INPUT
    def handle_input(self, player: PlayerProfile, choice:str):
        if choice == "1":
            random_number = random.randint(1, 100)
            if random_number <= 90:
                damage = player.char_class.attack
                self.monster.hp -= damage

                print(f"{player.name} attacks for {damage} damage!")
            else:
                print(f"{player.name} missed the attack!")
        elif choice == "2":
            random_number = random.randint(1, 100)
            if random_number <= 50:
                damage = player.char_class.attack * 1.2
                self.monster.hp -= damage

                print(f"{player.name} uses a heavy attack for {damage} damage!")
            else:
                print(f"{player.name} missed the heavy attack!")
        elif choice == "3":
            random_number = random.randint(1, 100)
            if random_number <= 10:
                damage = player.char_class.attack * 2
                self.monster.hp -= damage

                print(f"{player.name} uses a special attack for {damage} damage!")
            else:
                print(f"{player.name} missed the special attack!")
        else:
           return False
        return True
    #CLIs
    #ONLY USED FOR PRINTING CLI
    def status_bar_cli(self):
        print("\n==============================")
        print("Mob Hunt Adventure")
        print("==============================")
        print(f"Player 1: ({self.player1.name} {self.player1.char_class.name}) HP: {max(0, self.player1.char_class.hp)}")
        print(f"Player 2: ({self.player2.name} {self.player2.char_class.name}) HP: {max(0, self.player2.char_class.hp)}")
        print(f"Monster : ({self.monster.name}) HP: {max(0, self.monster.hp)}")
        print("\n==============================")

    def player_turn_cli(self, player: PlayerProfile):
        if player.char_class.hp <= 0:
            print(f"{player.name} is defeated and cannot take a turn.")
            return
        print(f"\n{player.name}'s turn")
        print("1. Attack")
        print("2. Heavy Attack")
        print("3. Special Attack")
        while True:
            choice = input("Enter your choice (1-3): ").strip()
            if self.handle_input(player, choice):
                break       
            else:
                print("Invalid choice. Please enter 1, 2, 3")
