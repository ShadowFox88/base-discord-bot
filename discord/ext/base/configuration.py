import pathlib
import tomllib
import typing

import pydantic

AnyDict: typing.TypeAlias = dict[str, typing.Any]

__all__ = ("CONFIGURATION", "Configuration")
CONFIGURATION = None
FILE = pathlib.Path("configuration.toml")


@pydantic.dataclasses.dataclass
class Configuration:
    PREFIX: str

    EXTENSIONS_FOLDER: str = pydantic.Field(default="", pattern=r"^([a-z_][a-z0-9_]*)(\.[a-z_][a-z0-9_]*)*$")
    JISHKAU: bool = False
    TOKEN: str = ""


with FILE.open("rb") as file_header:
    raw_configuration = tomllib.load(file_header)
    CONFIGURATION = Configuration(**raw_configuration)  # pyright: ignore[reportConstantRedefinition]
