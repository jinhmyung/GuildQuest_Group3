from typing import Optional

from adventure import AdventureMenu
from profileManager import ProfileManager
from gameSession import GameSession
from playerProfile import PlayerProfile
from user import User
import time
class GMAEEngine():
    def __init__(self):
        self.UserManager = User()
        self.player1 = None
        self.player2 = None
        self.menu = AdventureMenu()
        self.profile_manager = ProfileManager()
        self.session = Optional[GameSession]
        
        # these are the user option are they are printed in lines 36 and 37
        self.printOptions = ["EXIT", "Create user", "Login user 1", "Login user 2", "Realms (list/create)" ]
        
        # based on cmd input we index and call these methods in line 42
        self.CmdSelection = {
            "1": self.UserManager.create_cli, 
            "2": self.login_Player1,
            "3": self.login_Player2,
            "4": self.menu.show_options,
        }

    def run(self):
        cmd = None
        while cmd != "0":
            print("\n==============================")
            print("GuildQuest CLI")
            print("==============================")
            print(f"Player 1: {self.player1.name if self.player1 else '(none)'}")
            print(f"Player 2: {self.player2.name if self.player2 else '(none)'}")
            for num, option in enumerate(self.printOptions):
                print(f"{num}) {option}")
            #add in a try catch here for later
            cmd = input("Choose: ").strip()
            if cmd in self.CmdSelection.keys():
                self.CmdSelection[cmd]()
            
        print("Bye!")
    
    def login_attempt(self):
        # re-assigns player value 
        login_result = self.UserManager.login_cli()
        if login_result:
            time.sleep(2) # put this here becuase I want the user to see the result not scroll to see it 
            return login_result
        else:
            print("login failed please try again later")
            return None
    
    # this acts as an adapter and logs in player 1
    def login_Player1(self):
        self.player1 = self.login_attempt()


    # this acts as an adapter and logs in player 2 
    def login_Player2(self):
        self.player2 = self.login_attempt()


    def start_session(adventure_name: str, player1: PlayerProfile, player2: PlayerProfile):
        return
    
    def game_loop():
        return
    
    def end_session():
        return

