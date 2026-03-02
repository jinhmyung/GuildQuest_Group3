from abc import ABC, abstractmethod

class MiniAdventure(ABC):
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
    