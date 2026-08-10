import sys
from pydantic import ValidationError
from src.parsing.json_parsing import JsonParsing


class Main:
    def main() -> None:
        if len(sys.args) < 2:
            print("Argument error: missing json file")
            return
        if len(sys.args) > 2:
            print("Argument error: too many arguments entered")
            return

        try:
            json_parsing = JsonParsing(sys.args[1])

        except ValidationError as e:
            print(e.errors()[0]["msg"].replace("Value error, ", ""))
            return
        except (FileNotFoundError, ImportError, OSError) as e:
            print(f"File error: {e}")
            return
        except KeyboardInterrupt:
            print("\nCommand error: pacman has been interrupted")
            return
        except json.decoder.JSONDecodeError as e:
            print(f'Json format error:\n{e}')
            return


if __name__ == "__main__":
    try:
        main = Main()
        main.main()
    except Exception as e:
        print(f'Special error: {e}')
