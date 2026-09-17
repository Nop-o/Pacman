from pydantic import BaseModel, field_validator
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
    lives: int
    pacgum: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    super_pacgum_cooldown: int
    points_per_ghost: int
    level_max_time: int
    seed: int
    is_cheat_active: bool

    @field_validator("lives", mode="before")
    @classmethod
    def validate_lives(cls, v: Any) -> int:
        if not isinstance(v, int) or v < 0 or v > 200:
            print(f"Config file error: {v} is not a valid live count")
            return 3
        return v

    @field_validator("pacgum", mode="before")
    @classmethod
    def validate_pacgum(cls, v: Any) -> int:
        if not isinstance(v, int) or v < 1:
            print(f"Config file error: {v} is not a valid pacgum count")
            return 200
        return v

    @field_validator("points_per_pacgum", mode="before")
    @classmethod
    def validate_points_per_pacgum(cls, v: Any) -> int:
        if not isinstance(v, int) or v < -100000 or v > 100000:
            print(f"Config file error: {v} is not a valid point per pacgum")
            return 100
        return v

    @field_validator("points_per_super_pacgum", mode="before")
    @classmethod
    def validate_points_per_super_pacgum(cls, v: Any) -> int:
        if not isinstance(v, int) or v < -100000 or v > 100000:
            print(
                f"Config file error: {v} is not a valid point per super pacgum"
                )
            return 200
        return v

    @field_validator("super_pacgum_cooldown", mode="before")
    @classmethod
    def validate_super_pacgum_cooldown(cls, v: Any) -> int:
        if not isinstance(v, int) or v < 1 or v > 1000:
            print(
                f"Config file error: {v} is not a valid super pacgum cooldown")
            return 20
        return v

    @field_validator("points_per_ghost", mode="before")
    @classmethod
    def validate_points_per_ghost(cls, v: Any) -> int:
        if not isinstance(v, int) or v < -100000 or v > 100000:
            print(f"Config file error: {v} is not a valid point per ghost")
            return 500
        return v

    @field_validator("level_max_time", mode="before")
    @classmethod
    def validate_level_max_time(cls, v: Any) -> int:
        if not isinstance(v, int) or v < 20 or v > 1000000000:
            print(f"Config file error: {v} is not a valid level max time")
            return 90
        return v

    @field_validator("seed", mode="before")
    @classmethod
    def validate_seed(cls, v: Any) -> int:
        if not isinstance(v, int) or v < -1000000000 or v > 1000000000:
            print(f"Config file error: {v} is not a valid seed")
            return random.randint(-1000000000, 1000000000)
        return v

    @field_validator("is_cheat_active", mode="before")
    @classmethod
    def validate_is_cheat_active(cls, v: Any) -> bool:
        if v not in [
            True, 1, '1', 'true', 't', 'on', 'yes', 'y',
            False, 0, '0', 'false', 'f', 'off', 'no', 'n']:
            print(f"Config file error: {v} is not a valid cheat activation")
            return False
        return v
