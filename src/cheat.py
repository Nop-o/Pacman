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
        """Skip the current level when cheats are enabled."""
        if self.simulation_manager.game_state.is_cheat_active is False:
            return
        self.simulation_manager.screen_manager.game_play.next_level()

    def give_extra_lives(self) -> None:
        """Give the player one extra life."""
        if self.simulation_manager.game_state.is_cheat_active is False:
            return
        self.simulation_manager.game_state.current_lives += 1

    def change_invincibility(self) -> None:
        """Toggle player invincibility."""
        if self.simulation_manager.game_state.is_cheat_active is False:
            return
        self.is_invicible = not self.is_invicible

    def freeze_ghost(self) -> None:
        """Toggle ghost freezing."""
        if self.simulation_manager.game_state.is_cheat_active is False:
            return
        self.is_ghost_freeze = not self.is_ghost_freeze

    def freeze_timer(self) -> None:
        """Toggle timer freezing."""
        if self.simulation_manager.game_state.is_cheat_active is False:
            return
        self.is_timer_freeze = not self.is_timer_freeze
