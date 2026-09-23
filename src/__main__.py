import sys
from pydantic import ValidationError
from .parsing import JsonParsing, JsonData
from .visual_simulation import SimulationManager


class Main:
    """Entry point launching the Pac-Man application from the command line."""

    def main(self) -> None:
        """Parse the JSON config file argument and run the game.

        Reads the configuration file path from the command line, validates
        it, and runs the simulation. Errors are caught and printed as
        user-friendly messages rather than propagated.
        """
        if len(sys.argv) < 2:
            print("Argument error: missing json file")

        if len(sys.argv) > 2:
            print("Argument error: too many arguments entered")
            return

        try:
            if len(sys.argv) < 2:
                json_parsing = JsonParsing("config.json")
            else:
                json_parsing = JsonParsing(sys.argv[1])

            pacman_data = JsonData(**json_parsing.file_content)

        except ValidationError as e:
            error = e.errors()[0]
            print(f"{error['msg']}: missing {error["loc"][0]} key")
        except (FileNotFoundError, ImportError, OSError, ValueError) as e:
            print(f"File error: {e}")
            return

        try:
            simulation_manager = SimulationManager(pacman_data)
            simulation_manager.launch()
            simulation_manager.screen_manager.leaderboard.export_highscore()
        except KeyboardInterrupt:
            print("\nCommand error: pacman has been interrupted")
            return


if __name__ == "__main__":
    try:
        main = Main()
        main.main()
    except Exception as e:
        print(f'Special error: {e}')
