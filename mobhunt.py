from miniAdventure import MiniAdventure
from playerProfile import PlayerProfile
import random


class MobHunt(MiniAdventure):

    class Monster():
        def __init__(self, name:str, hp:int, attack:int):
            self.name = name
            self.hp = hp
            self.attack = attack

    def __init__(self, player1: PlayerProfile, player2: PlayerProfile, id: str):
        super().__init__(id)
        self.state = "ongoing"
        self.turn = 1
        self.result = None
        self.player1 = player1
        self.player2 = player2
        self.monster = self.Monster("Goblin", 100, 20)
        self.player_choice = {"1": 80, "2": 60, 20:2}
        self.RandomScale = {80: 1, 60: 1.2, 20: 2}

    def handle_input(self, player: PlayerProfile, choice:str):
        if choice == "1":
            random_number = random.randint(1, 100)
            if random_number >= 80:
                damage = player.char_class.attack
                self.monster.hp -= damage

                print(f"{player.name} attacks for {damage} damage!")
            else:
                print(f"{player.name} missed the attack!")
        elif choice == "2":
            random_number = random.randint(1, 100)
            if random_number >= 60:
                damage = player.char_class.attack * 1.2
                self.monster.hp -= damage

                print(f"{player.name} uses a heavy attack for {damage} damage!")
            else:
                print(f"{player.name} missed the heavy attack!")
        elif choice == "3":
            random_number = random.randint(1, 100)
            if random_number >= 20:
                damage = player.char_class.attack * 2
                self.monster.hp -= damage

                print(f"{player.name} uses a special attack for {damage} damage!")
            else:
                print(f"{player.name} missed the special attack!")
        else:
           return False
        return True

    def update(self):
        return
    
    def get_state(self):
        return self.state

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


    def get_result(self):
        return self.result

    def reset(self):
        self.state = "not started"
        self.result = None


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
                print("Invalid choice. Please enter 1, 2, or 3.")

    def monster_turn_cli(self):
        print(f"\n{self.monster.name}'s turn")
        target = random.choice([self.player1, self.player2])
        while target.char_class.hp <= 0:
            target = random.choice([self.player1, self.player2])
        damage = self.monster.attack
        print(f"{self.monster.name} attacks {target.name} for {damage} damage!")
        target.char_class.hp -= damage

    # changed this method name since it should probably be the same for both miniAdventures
    def start_adventure(self):
        print("\n==============================")
        print("Mob Hunt Adventure")
        print("==============================")
        print(f"Player 1: {self.player1.name} ({self.player1.char_class})")
        print(f"Player 2: {self.player2.name} ({self.player2.char_class})")
        print(f"Monster : {self.monster.name})")
        print("\n==============================")
        while True:
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
