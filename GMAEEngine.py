from typing import Optional

from adventure import AdventureMenu, DictOfAdventureMenu
from profileManager import ProfileManager
from gameSession import GameSession
from playerProfile import PlayerProfile
from user import User
from RealmRegister import RealmRegister, RealmCoord
import time
        
        
TEST_MODE = False

class GMAEEngine():
    def __init__(self):

        self.UserManager = User()
        self.player1 = None
        self.player2 = None
        self.DictOfAdventureMenu = DictOfAdventureMenu().AM_dictionary #key: Realm, value: AdventureMenu
        self.currentMenu = AdventureMenu()
        self.profile_manager = ProfileManager()
        self.session = Optional[GameSession]
        
        self.realmReg = RealmRegister().realms
        self.currentRealm = self.realmReg[RealmCoord(0,0)] #Realms created in RealmRegister
        self.DictOfAdventureMenu[self.currentRealm] = self.currentMenu
        



        
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
            

            print(f"Current Realm: {self.currentRealm.name} (x: {self.currentRealm.Coord.x}, y: {self.currentRealm.Coord.y})")
            print(f"Player 1: {self.player1.name if self.player1 else '(none)'}")
            print(f"Player 2: {self.player2.name if self.player2 else '(none)'}")

            for num, option in enumerate(self.printOptions):
                print(f"{num}) {option}")
            cmd = input("Choose: ").strip()
            
            if cmd in self.CmdSelection.keys():
                self.CmdSelection[cmd]()
            elif cmd != "0":
                print("Invalid option. Please enter 0, 1, 2, 3, 4, 5, 6, or 7.")
            
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
        if TEST_MODE:
            self.player1 = self.UserManager.TEST_LOGIN_P1()
        else:
            self.player1 = self.login_attempt()
        if self.player1:
            
            print("Player 1 logged in mmmmm.")

    # this acts as an adapter and logs in player 2
    def login_Player2(self):
        if TEST_MODE:
            self.player2 = self.UserManager.TEST_LOGIN_P2()
        else:
            self.player2 = self.login_attempt()
        if self.player2:
            print("Player 2 logged in.")

    def PrintOptions(self, list_obj): #MARKED FOR JIN's REFERENCE
        print(f"what would you like to do? (enter 0 to end) :") 
        for num, obj in enumerate(list_obj):
            print(f"{num + 1} : {obj}")
        
        result = input().strip()
        while result != "0":
            if result.isdigit() and int(result) <= len(list_obj):
                print(f"selected result {list_obj[int(result) - 1]}")
                return int(result) - 1
            else:
                print("THAT GAME DOES NOT EXIST! (TRY AGAIN)")
            result = input().strip()
        

    def start_session(self):
        if self.player1 and self.player2:
            # get the mini game option's ex Mobhunt/treasureTrap
            miniGames = self.currentMenu.show_options()
            # call the method in line 79 and pass in the mini game options to be printed also get user input and it's result
            result = self.PrintOptions(miniGames)

            # create an instance of the chosen game pass in game name, player1, player2, some stringID this case doesn't matter. 
            self.currentMenu.get_selections(miniGames[result], self.player1, self.player2, miniGames[result], self.currentRealm)
        
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
<<<<<<< HEAD
        cmd = input("Enter Realm Coordinates: \"x y\"\n").strip()
        try:
            coord = cmd.split()
            x = int(coord[0])
            y = int(coord[1])
        except ValueError:
            print("Coordinates must be numbers.")
        try:
            self.currentRealm = self.realmReg[RealmCoord(x,y)]
            print("Entered Realm Successfully")
        except Exception as E:
            print("Realm doesn't exist")
=======
        cmd = input("Enter Realm Coordinates: \"x y\" (0 to go back)\n").strip()
        while cmd != "0":
            try:
                coord = cmd.split()
                x = int(coord[0])
                y = int(coord[1])
                try:
                    self.currentRealm = self.realmReg[RealmCoord(x,y)]
                    self.currentMenu = self.DictOfAdventureMenu[self.currentRealm]
                    print("Entered Realm Successfully")
                    break
                except Exception as E:
                    print("Realm doesn't exist")
            except ValueError:
                print("Coordinates must be numbers.")
            except IndexError:
                print("Please enter a coordinate in range in the form x y (eg. 1 0)")
            cmd = input("Enter Realm Coordinates: \"x y\" (0 to go back)\n").strip()
>>>>>>> b56bf1c520c5550cde2841727cfdde69005068fb

        #JIn will implement realm switching mechanics here. Reminder to me to change current_realm and miniAdventure_menu to corresponding Realm
        return

    def _show_inventory(self, profile, label: str) -> None:
        print(f"\n----- {label} Inventory -----")
        if profile is None:
            print(f"{label} is not logged in.")
            input("Press Enter to continue...")
            return
        print(f"Player: {profile.name}")
        inv = getattr(profile, "inventory", [])
        # profile has self.inventory and if we call getAllItems() on it then we get a list
        inv = inv.getAllItems()

        if not inv:
            print("  (empty)")
        else:
            for i, it in enumerate(inv, 1):
                name = it.get("name", "?") if isinstance(it, dict) else getattr(it, "name", "?")
                rarity = it.get("rarity", "") if isinstance(it, dict) else getattr(it, "rarity", "")
                item_type = it.get("item_type", "") if isinstance(it, dict) else getattr(it, "item_type", "")
                print(f"  {i}. {name}  [{item_type}]  ({rarity})")
        print("==============================")
        input("Press Enter to continue...")

    def view_p1_inventory(self) -> None:
        print(type(self.player1))
        self.player1.addItem()
        self._show_inventory(self.player1, "P1")

    def view_p2_inventory(self) -> None:
        self._show_inventory(self.player2, "P2")

    
    def game_loop():
        return
    
    def end_session():
        return

