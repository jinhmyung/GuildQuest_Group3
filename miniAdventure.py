from abc import ABC, abstractmethod

class MiniAdventure(ABC):

    def __init__(self, id: str): # for the trigger_adventureID in realm.py
        self.id = id

    @abstractmethod
    def initialize(self): 
        return
    @abstractmethod
    def handle_input(self, player_input:str):
        return
    @abstractmethod
    def update(self):
        return
    @abstractmethod
    def get_state():
        return
    @abstractmethod
    def is_finished(self):
        return
    @abstractmethod
    def get_result(self):
        return
    @abstractmethod
    def reset(self):
        return

    @abstractmethod
    def start_adventure(self):
        pass
