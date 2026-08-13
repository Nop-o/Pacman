from .screen import Screen
from .level import Level
from .hud import HUD


class GamePlay(Screen):
    def __init__(self, level: Level, hud: HUD) -> None:
        self.level: Level = level
        self.hud: HUD = hud

    def display_screen(self) -> None:
        self.level.display_screen()
        self.hud.display_screen()

    def event_manager(self) -> bool:  # TODO
        pass
