from abc import ABC, abstractmethod


class Screen(ABC):

    @abstractmethod
    def display_screen(self) -> None: ...
