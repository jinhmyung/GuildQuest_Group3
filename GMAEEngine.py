from typing import Optional

from adventure import AdventureMenu
from profileManager import ProfileManager
from gameSession import GameSession
from playerProfile import PlayerProfile
from user import User
    
class GMAEEngine():
    def __init__(self):
        self.UserManager = User()
        self.player1 = None
        self.player2 = None
        self.menu = AdventureMenu()
        self.profile_manager = ProfileManager()
        self.session = Optional[GameSession]

    def run(self):
        while True:
            print("\n==============================")
            print("GuildQuest CLI")
            print("==============================")
            print(f"Player 1: {self.player1.name if self.player1 else '(none)'}")
            print(f"Player 2: {self.player2.name if self.player2 else '(none)'}")
            print("1) Create user")
            print("2) Login user 1")
            print("3) Login user 2")
            print("4) Realms (list/create)") #should print error message if both user aren't logged in
            # print("11) Save") we'll make it save automatically 
            # print("12) Load") we'll make it load after user logins
            print("0) Exit")
            cmd = input("Choose: ").strip()
            if cmd == "1":
                self.UserManager.create_cli()
            elif cmd == "2":
                login_result = self.UserManager.login_cli()
                if login_result:
                    self.player1 = login_result
            elif cmd == "3":
                login_result = self.UserManager.login_cli()
                if login_result:
                    self.player2 = login_result
            elif cmd == "4":
                return
                # menu_realms()
            elif cmd == "0":
                print("Bye!")
                return
    
    def start_session(adventure_name: str, player1: PlayerProfile, player2: PlayerProfile):
        return
    
    def game_loop():
        return
    
    def end_session():
        return

