from abc import ABC, abstractmethod
from ..screen_manager import ScreenManager


class Screen(ABC):
    def __init__(self, screen_manager: ScreenManager) -> None:
        self.screen_manager: screen_manager = screen_manager

    @abstractmethod
    def display_screen(self) -> bool: ...

    @abstractmethod
    def event_manager(self) -> bool: ...

    def exit_game(self) -> bool:
        return False

    def go_to_main_menu(self) -> bool:
        return self.screen_manager.main_menu.display_screen()

    def resume_game(self) -> bool:
        return self.screen_manager.game_play.display_screen()

    def show_leaderboard(self) -> bool:
        return self.screen_manager.leaderboard.display_screen()

    def start_game(self) -> bool:
        return self.screen_manager.game_play.display_screen()
