import json
import random
import os #issues with finding the file on my side so had to os.getcwd()
from profileManager import ProfileManager



class User():


    def __init__(self, fileName = "user.json"):
        self.fileName = fileName
        self.profile_manager = ProfileManager()
        self.JsonFilePath = os.path.join(os.getcwd(), fileName)
        self.TestBoolPlayer1 = True


    def create_user(self, username: str, password: str) -> None:
        try:
            
            with open(self.JsonFilePath, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("unable to save user at this moment")
            data = {}
    
        if username in data:
            print("User already exists!")
            return False
            
        profile_id = f"{username}_{random.randint(1000, 9999)}"
        self.profile_manager.create_profile(profile_id)

        data[username] = {
            "profile_id": profile_id,
            "password": password
        }
        with open(self.JsonFilePath, "w") as f:
            json.dump(data, f, indent = 2)
        return True
        
    def login(self, username: str, password: str) -> int:

        with open(self.JsonFilePath, "r") as f:
            data = json.load(f)
            if username in data and data[username]["password"] == password:
                #print("Profile Username: " + username)
                profile_id = data[username]["profile_id"]
                #print("Profile ID" + profile_id)
                return self.profile_manager.load(profile_id)
        return False

    def TEST_LOGIN(self):
        """remove this when we submit it is so we don't have to login every time"""
        if self.TestBoolPlayer1:
            self.TestBoolPlayer1 = False
            return self.login("ydureix", "something123")
        else:
            return self.login("Criminal", "crimes123")

    def TEST_LOGIN_P1(self):
        """Always log in as player 1 test account (ydureix/John)."""
        return self.login("ydureix", "something123")

    def TEST_LOGIN_P2(self):
        """Always log in as player 2 test account (Criminal/Crime)."""
        return self.login("Criminal", "crimes123")


        

    def login_cli(self):
        while True:
            print("\n==============================")
            print("GuildQuest CLI")
            print("==============================")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            login_result = self.login(username, password)

            if not login_result:
                print("Invalid username or password.")
                return False
            
            else:
                print("Login successful!")
                return login_result
    
    def create_cli(self):
        while True:
            print("\n==============================")
            print("GuildQuest CLI")
            print("==============================")
            username = input("Choose a username: ").strip()
            password = input("Choose a password: ").strip()
            
            
            create_result = self.create_user(username, password)
            if create_result:
                print("User created successfully!")
            else:
                print("User creation failed. Try again.")
            return 