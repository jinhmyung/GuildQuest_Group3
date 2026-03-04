if __name__ == "__main__":


    def run(self) -> None:
        # self.ensure_default_realm()
        while True:
            print("\n==============================")
            print("GuildQuest CLI")
            print("==============================")
            print(f"Current user: {self.current_user if self.current_user else '(none)'}")
            print("1) Create user")
            print("2) Login user 1")
            print("3) Login user 2")
            print("4) Realms (list/create)") #should print error message if both user aren't logged in
            # print("11) Save") we'll make it save automatically 
            # print("12) Load") we'll make it load after user logins
            print("0) Exit")
            cmd = input("Choose: ").strip()
            if cmd == "1":
                self.create_user()
            elif cmd == "2":
                self.login_user1()
            elif cmd == "3":
                self.login_user2()
            elif cmd == "4":
                self.menu_realms()
            elif cmd == "0":
                print("Bye!")
                return