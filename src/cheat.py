from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .visual_simulation import SimulationManager


class Cheat:
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        self.simulation_manager: "SimulationManager" = simulation_manager
        self.is_invicible: bool = False
        self.is_ghost_freeze: bool = False
        self.is_timer_freeze: bool = False

    def skip_level(self) -> None:
        if self.simulation_manager.game_state.is_cheat_active is False:
            return
        self.simulation_manager.screen_manager.game_play.next_level()

    def give_extra_lives(self) -> None:
        if self.simulation_manager.game_state.is_cheat_active is False:
            return
        self.simulation_manager.game_state.current_lives += 1

    def change_invincibility(self) -> None:
        if self.simulation_manager.game_state.is_cheat_active is False:
            return
        if self.is_invicible is True:
            self.is_invicible = False
        else:
            self.is_invicible = True

    def freeze_ghost(self) -> None:
        if self.simulation_manager.game_state.is_cheat_active is False:
            return
        if self.is_ghost_freeze is True:
            self.is_ghost_freeze = False
        else:
            self.is_ghost_freeze = True

    def freeze_timer(self) -> None:
        if self.simulation_manager.game_state.is_cheat_active is False:
            return
        if self.is_timer_freeze is True:
            self.is_timer_freeze = False
        else:
            self.is_timer_freeze = True

