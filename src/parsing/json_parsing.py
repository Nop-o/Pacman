from pydantic import Field, BaseModel
import json5
from typing import Any
import random


class JsonParsing:

    def __init__(self, file_path: str) -> None:
        self.file_content: Any = self._load_json_file(file_path)

    def _load_json_file(self, file_path: str) -> Any:
        """Load json content"""
        if not file_path.endswith(".json"):
            raise ValueError("Argument error: file is not a json file")

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        filtered: list[str] = [
            line for line in lines if not line.lstrip().startswith('#')]
        hashtag_less_content: list[str] = [
            line.split('#', 1)[0] for line in filtered]

        self._verify_duplicate_keys(hashtag_less_content)

        file_content: str = "".join(hashtag_less_content)

        return json5.loads(file_content)

    @staticmethod
    def _verify_duplicate_keys(data: list[str]) -> None:
        """Verify duplicate keys"""
        registered_keys = set()

        for line in data:
            if ':' in line:
                key = line.split(':')[0]
                if key in registered_keys:
                    raise ValueError("Key error: duplicate keys entered")

                registered_keys.add(key)


class JsonData(BaseModel):
    lives: int = Field(ge=0, le=200)
    pacgum: int = Field(ge=1)
    points_per_pacgum: int = Field(ge=-100000, le=100000)
    points_per_super_pacgum: int = Field(ge=-100000, le=100000)
    super_pacgum_cooldown: int = Field(ge=1, le=1000)
    points_per_ghost: int = Field(ge=-100000, le=100000)
    level_max_time: int = Field(ge=20, le=1000000000)
    seed: int = Field(default=random.randint(-1000000000, 1000000000),
                      ge=-1000000000, le=1000000000)
    is_cheat_active: bool = Field(default=False)
