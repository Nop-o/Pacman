from pydantic import (BaseModel, field_validator, ConfigDict, Field,
                      ValidatorFunctionWrapHandler, ValidationInfo,
                      model_validator, ValidationError)
import json5
from typing import Any
import random
import sys


class JsonParsing:
    """Load a JSON file that may contain comments and reject duplicate keys."""

    def __init__(self, file_path: str) -> None:
        """Load the content of a JSON file.

        Args:
            file_path: Path of the JSON file to load. It must end with
                `.json`.
        """
        self.file_content: Any = self._load_json_file(file_path)

    def _load_json_file(self, file_path: str) -> Any:
        """Read a JSON file and parse its content.

        Everything after a `#` on a line is treated as a comment and
        removed before parsing. The content is parsed with `json5`, and
        duplicate keys in an object are rejected.

        Args:
            file_path: Path of the JSON file to read. It must end with
                `.json`.

        Returns:
            The parsed content of the file.
        """
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
        """Build a dict from the key-value pairs of a JSON object.

        Used as the `object_pairs_hook` of the parser, so it is called
        for every object found in the file.

        Args:
            pairs: The `(key, value)` pairs of one JSON object, in the
                order they appear in the file.

        Returns:
            A dict made from the pairs.
        """
        result: dict[str, Any] = {}

        for key, value in pairs:
            if key in result:
                raise ValueError(f"Key error: duplicate key '{key}'")

            result[key] = value

        return result


class JsonData(BaseModel):
    """The game settings read from the JSON file.

    Unknown keys are rejected, and values are validated again when they
    are assigned.
    A missing or invalid value is replaced by the default
    value of its field, with a message printed.

    Attributes:
        lives: Number of lives (1 to 200, default 3).
        pacgum: Number of pac-gums (1 to 100000, default 200).
        points_per_pacgum:
            Points for a pac-gum (-100000 to 100000, default 200)
        points_per_super_pacgum:
            Points for a super pac-gum (-100000 to 100000, default 500)
        super_pacgum_cooldown:
            Cooldown of the super pac-gum (1 to 1000, default 20)
        points_per_ghost:
            Points for a ghost (-100000 to 100000, default 1000)
        level_max_time:
            Maximum time of a level (20 to 100000, default 90).
        seed: Random seed (-100000 to 100000)
        is_cheat_active: Whether the cheat mode is active (default False)
    """

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
        """Replace an invalid field value with the default of the field.

        Runs on every field. If the value isn't valid, a message is printed and
        the default value of the field is used.

        Args:
            value: The value read from the file for the field.
            handler: The standard validation of the field.
            info: Information about the field being validated.

        Returns:
            The validated value, or the default value of the field if
            the value is invalid.
        """
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
                f"Using pydantic default value ({default})", file=sys.stderr)
            return default

    @model_validator(mode="after")
    def verify_missing_key(self) -> 'JsonData':
        """Print a message for each field missing from the input.

        Missing fields keep their default value, so the model is
        returned unchanged.

        Returns:
            The validated model.
        """
        for name, field in type(self).model_fields.items():
            if name not in self.model_fields_set:
                print(
                    f"Parsing error: key '{name}' is missing.\n"
                    "Using pydantic default value "
                    f"({field.get_default(call_default_factory=True)})",
                    file=sys.stderr)
        return self
