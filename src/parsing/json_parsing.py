from pydantic import (BaseModel, field_validator, ConfigDict, Field,
                      ValidatorFunctionWrapHandler, ValidationInfo,
                      model_validator, ValidationError)
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

        filtered_lines: list[str] = [
            line.split('#', 1)[0].strip() for line in lines]

        file_content: str = "\n".join(filtered_lines)

        return json5.loads(
            file_content, object_pairs_hook=self._verify_duplicate_keys)

    @staticmethod
    def _verify_duplicate_keys(pairs: Any) -> Any:
        result: dict[str, Any] = {}

        for key, value in pairs:
            if key in result:
                raise ValueError(f"Key error: duplicate key '{key}'")

            result[key] = value

        return result


class JsonData(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    lives: int = Field(default=3, ge=1, le=200)
    pacgum: int = Field(default=200, ge=1, le=100000)
    points_per_pacgum: int = Field(default=200, ge=-100000, le=100000)
    points_per_super_pacgum: int = Field(default=500, ge=-100000, le=100000)
    super_pacgum_cooldown: int = Field(default=20, ge=1, le=1000)
    points_per_ghost: int = Field(default=1000, ge=-100000, le=100000)
    level_max_time: int = Field(default=90, ge=20, le=100000)
    seed: int = Field(
        default_factory=lambda: random.randint(-100000, 100000),
        ge=-100000, le=100000)
    is_cheat_active: bool = Field(default=False)

    @field_validator("*", mode="wrap")
    @classmethod
    def clamp_all(cls, value: Any,
                  handler: ValidatorFunctionWrapHandler,
                  info: ValidationInfo) -> Any:
        try:
            return handler(value)
        except ValidationError:
            if info.field_name is None:
                raise ValueError("Pydantic error: `info.field_name` is `None`")

            default = cls.model_fields[info.field_name].get_default(
                call_default_factory=True)
            print(
                f"Parsing error: '{info.field_name}' has an invalid "
                f"value ({value})\n"
                f"Using pydantic default value ({default})")
            return default

    @model_validator(mode="after")
    def verify_missing_key(self) -> 'JsonData':
        for name, field in type(self).model_fields.items():
            if name not in self.model_fields_set:
                print(
                    f"Parsing error: key '{name}' is missing.\n"
                    "Using pydantic default value "
                    f"({field.get_default(call_default_factory=True)})")
        return self
