from .screen import Screen
from .hud import HUD


class GamePlay(Screen):
    def __init__(self, level, hud: HUD) -> None:
        self.level = level
        self.hud: HUD = hud

    def display_screen(self) -> bool:
        self.level.display_screen()
        self.hud.display_screen()

    def event_manager(self) -> bool:  # TODO
        pass
