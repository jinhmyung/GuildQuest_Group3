from typing import Optional

from adventure import AdventureMenu
from profileManager import ProfileManager
from gameSession import GameSession
from playerProfile import PlayerProfile
from user import User
from RealmRegister import RealmRegister, RealmCoord
import time

TEST_MODE = True
class GMAEEngine():
    def __init__(self):
        self.UserManager = User()
        self.player1 = None
        self.player2 = None
        self.menu = AdventureMenu()
        self.profile_manager = ProfileManager()
        self.session = Optional[GameSession]
        
        self.realmReg = RealmRegister().realms
        self.currentRealm = self.realmReg[RealmCoord(0,0)] #Realms created in RealmRegister
        



        
        # these are the user option are they are printed in lines 36 and 37
        self.printOptions = ["EXIT", "Create user", "Login user 1", "Login user 2", "MiniAdventure Menu", "Move Realm", "View P1 inventory", "View P2 inventory"]
        
        # based on cmd input we index and call these methods in line 42
        self.CmdSelection = {
            "1": self.UserManager.create_cli, 
            "2": self.login_Player1,
            "3": self.login_Player2,
            "4": self.start_session,
            "5": self.move_realms,
            "6": self.view_p1_inventory,
            "7": self.view_p2_inventory,
        }

    def run(self):
        cmd = None
        while cmd != "0":
            print("\n==============================")
            print("GuildQuest CLI")
            print("TEST MODE SET UP")
            print("==============================")
            
            # TEST MODE REMOVE BEDORE SUBMITING
            if TEST_MODE:
                self.login_Player1()
                self.login_Player2()
                TEST_LOGIN = False
            

            print(f"Current Realm: {self.currentRealm.name} (x: {self.currentRealm.Coord.x}, y: {self.currentRealm.Coord.x})")
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
        self.player1 = self.UserManager.TEST_LOGIN()
        #self.player1 = self.login_attempt()


    # this acts as an adapter and logs in player 2 
    def login_Player2(self):
        self.player2 = self.UserManager.TEST_LOGIN()

        #self.player2 = self.login_attempt()

    def PrintOptions(self, list_obj): #MARKED FOR JIN's REFERENCE
        print(f"what would you like to do? (enter 0 to end) :") 
        for num, obj in enumerate(list_obj):
            print(f"{num} : {obj}")
        
        result = input().strip()
        if result.isdigit() and int(result) < len(list_obj):
            print(f"selected result {list_obj[int(result)]}")
            return int(result)

    def start_session(self):
        if self.player1 and self.player2:
            # get the mini game option's ex Mobhunt/treasureTrap
            miniGames = self.menu.show_options()
            # call the method in line 79 and pass in the mini game options to be printed also get user input and it's result
            result = self.PrintOptions(miniGames)

            # create an instance of the chosen game pass in game name, player1, player2, some stringID this case doesn't matter. 
            self.menu.get_selections(miniGames[result], self.player1, self.player2, miniGames[result])
        
        return
    

    
    def show_realms(self): #default realms initialized in init RealmRegister
        print("\n==============================")
        print("Realms: \n")

        realm_counter = 1
        for realm in self.realmReg.values():
            print(f"{realm_counter}: {realm.name} | Description: {realm.description} | Coord:{realm.Coord.x},{realm.Coord.y}")
            realm_counter+=1

        # print("\nEnter Realm Number: ")
        print("==============================\n")

    def move_realms(self): #
        self.show_realms()
        print("Move commands: \"left\", \"right\", \"up\", \"down\"")
        #JIn will implement realm switching mechanics here. Reminder to me to change current_realm and miniAdventure_menu to corresponding Realm
        return

    def _show_inventory(self, profile, label: str) -> None:
        if profile is None:
            print(f"{label} is not logged in.")
            return
        print(f"\n===== {label} Inventory ({profile.name}) =====")
        inv = getattr(profile, "inventory", [])
        if not inv:
            print("  (empty)")
        else:
            for i, it in enumerate(inv, 1):
                name = it.get("name", "?") if isinstance(it, dict) else getattr(it, "name", "?")
                rarity = it.get("rarity", "") if isinstance(it, dict) else getattr(it, "rarity", "")
                item_type = it.get("item_type", "") if isinstance(it, dict) else getattr(it, "item_type", "")
                print(f"  {i}. {name}  [{item_type}]  ({rarity})")
        print("==============================\n")

    def view_p1_inventory(self) -> None:
        self._show_inventory(self.player1, "P1")

    def view_p2_inventory(self) -> None:
        self._show_inventory(self.player2, "P2")

    
    def game_loop():
        return
    
    def end_session():
        return

