from pydantic import Field, BaseModel
import json
import os
from typing import Any


class JsonParsing:

    def __init__(self, file_path: str,
                 temp_file_path: str = "temp_file.json") -> None:
        self.file_content: Any = self._load_json_file(
            file_path, temp_file_path)

    def _load_json_file(self, file_path: str, temp_file_path: str) -> Any:
        """Load json content"""
        if not file_path.endswith(".json"):
            raise ValueError("Argument error: file is not a json file")

        if file_path == temp_file_path:
            raise ValueError(
                "Parsing error: error removing comments from json file")

        self._create_temp_file(file_path, temp_file_path)

        with open(temp_file_path, "r", encoding="utf-8") as f:
            file_content = json.load(
                f, object_pairs_hook=JsonParsing._verify_duplicate_keys)

        os.remove(temp_file_path)

        return file_content

    @staticmethod
    def _verify_duplicate_keys(data: list[tuple[Any, Any]]) -> Any:
        """Verify duplicate keys"""
        registered_keys = {}

        for key, val in data:
            if key in registered_keys:
                raise ValueError("Key error: duplicate keys entered")
            registered_keys[key] = val

        return registered_keys

    def _create_temp_file(self, to_copy_file_path: str,
                          new_file_path: str) -> None:
        """Create a temp file without the comments"""
        comments: tuple[str, str] = ("//", "#")
        file_content_without_comments: str = ""

        with open(to_copy_file_path, "r") as f:
            file_content: list[str] = f.readlines()

        for line in file_content:
            line = line.strip()
            if not line:
                continue

            for comment in comments:
                if comment in line:
                    line = line.split(comment, 1)[0]
                    break

            if line:
                file_content_without_comments = (
                    file_content_without_comments + line)

        with open(new_file_path, "w", encoding="utf-8") as file:
            file.write(file_content_without_comments)


class JsonData(BaseModel):
    highscore_filename: str = Field(min_length=1, max_length=100)
    level: list
    width: int = Field(ge=0, le=200)
    height: int = Field(ge=0, le=200)
    lives: int = Field(ge=0, le=200)
    pacgum: int = Field(ge=0)
    points_per_pacgum: int = Field(ge=-100000, le=100000)
    points_per_super_pacgum: int = Field(ge=-100000, le=100000)
    points_per_ghost: int = Field(ge=-100000, le=100000)
    seed: int = Field(ge=-1000000000, le=1000000000)
    level_max_time: int = Field(ge=20, le=1000000000)


if __name__ == "__main__":
    parser = JsonParsing("settings.json", "setting.json")
    print(parser.file_content)
