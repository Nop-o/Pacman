from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .visual_simulation import SimulationManager


class Cheat:
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        self.simulation_manager: "SimulationManager" = simulation_manager
        self.invicibility: bool = False
        self.ghost_freeze: bool = False

    # TODO
    def skip_level(self) -> None:
        pass

    def give_extra_lives(self) -> None:
        self.simulation_manager.game_state.current_lives += 1

    def turn_on_invincibility(self) -> None:
        self.invicibility = True

    def turn_off_invincibility(self) -> None:
        self.invicibility = False

    # TODO
    def increase_speed(self) -> None:
        pass

    # TODO
    def slow_speed(self) -> None:
        pass
