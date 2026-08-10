import sys
from pydantic import ValidationError
from parsing.json_parsing import JsonParsing
import json


class Main:
    def main(self) -> None:
        if len(sys.argv) < 2:
            print("Argument error: missing json file")
            return
        if len(sys.argv) > 2:
            print("Argument error: too many arguments entered")
            return

        try:
            json_parsing = JsonParsing(sys.argv[1])
            print(json_parsing.file_content)

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
