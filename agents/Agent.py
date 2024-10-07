from abc import ABC, abstractmethod
from typing import Iterable

class Agent(ABC):

    def __init__(self, type: str) -> None:
        self.type = type


    @abstractmethod
    def run(self, user_input) -> str:
        pass

    @abstractmethod
    def run_stream(self, user_input) -> Iterable[str]:
        pass
