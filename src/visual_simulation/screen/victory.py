from . import LeaderBoard, Screen
from .. import SimulationManager
import pygame


class Victory(Screen):
    def __init__(self, score: int, simulation: SimulationManager) -> None:
        self.score: int = score
        self.simulation_manager

    def display_screen(self) -> None:  # TODO
        pass
