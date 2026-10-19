import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


class Main:
    """Entry point launching the Pac-Man application from the command line."""

    @staticmethod
    def main() -> None:
        """Parse the JSON config file argument and run the game.

        Reads the configuration file path from the command line, validates
        it, and runs the simulation. Errors are caught and printed as
        user-friendly messages rather than propagated.
        """
        from pydantic import ValidationError
        from .parsing import JsonParsing, JsonData
        from .visual_simulation import SimulationManager

        if len(sys.argv) > 2:
            print("Argument error: too many arguments entered",
                  file=sys.stderr)
            return

        try:
            if len(sys.argv) < 2:
                json_parsing = JsonParsing("config.json")
            else:
                json_parsing = JsonParsing(sys.argv[1])

            if not isinstance(json_parsing.file_content, dict):
                raise ValueError("Data error: invalid json data type")
            pacman_data = JsonData(**json_parsing.file_content)

        except ValidationError as e:
            error = e.errors()[0]
            print(f"{error['msg']}: missing {error["loc"][0]} key",
                  file=sys.stderr)
            return
        except (FileNotFoundError, ImportError, OSError, ValueError) as e:
            print(f"File error: {e}", file=sys.stderr)
            return

        simulation_manager = SimulationManager(pacman_data)
        simulation_manager.launch()
        simulation_manager.screen_manager.leaderboard.export_highscore()


if __name__ == "__main__":
    try:
        Main.main()
    except Exception as e:
        print(f'Special error: {e}', file=sys.stderr)
    except KeyboardInterrupt:
        print("\nCommand error: pacman has been interrupted", file=sys.stderr)
