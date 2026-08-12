from time import time, sleep
import pygame
from collections.abc import Callable

class SimulationManager():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Pac-Man")
        self.fps: int = 60
        self.frame_duration: float = 1.0 / self.fps
        self.screen: pygame.Surface = pygame.display.set_mode((1500, 1000))
        # TODO set basic function to main menu
        self.test = Test(self)
        self.state_to_call: Callable = self.test.test1
        self.active = True

    def launch(self) -> None:
        while self.active:
            start_time = time()
            self.state_to_call()
            pygame.display.flip()

            self.event_manager()
            elapsed = time() - start_time
            if elapsed < self.frame_duration:
                sleep(self.frame_duration - elapsed)

    def event_manager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # TODO call menu
                    pass


if __name__ == "__main__":
    class Test():
        def __init__(self, simulation_manager: SimulationManager) -> None:
            self.simulation_manager = simulation_manager
            self.color: tuple = (0, 0, 0)
        def test1(self):
            screen = self.simulation_manager.screen
            screen.fill("black")
            
            size = 50
            for dx in range(size):
                for dy in range(size):
                    screen.set_at((500 + dx, 500 + dy), self.color)
            
            self.color = (self.color[0] + 1,
                        self.color[1] + 1,
                        self.color[2] + 1)
            if self.color[0] == 255:
                self.simulation_manager.state_to_call = self.test2
        def test2(self):
            screen = self.simulation_manager.screen
            screen.fill("white")
            
            size = 50
            for dx in range(size):
                for dy in range(size):
                    screen.set_at((500 + dx, 500 + dy), self.color)
            
            self.color = (self.color[0] - 1,
                        self.color[1] - 1,
                        self.color[2] - 1)
            if self.color[0] == 0:
                self.simulation_manager.state_to_call = self.test1
    simulation = SimulationManager()
    simulation.launch()
