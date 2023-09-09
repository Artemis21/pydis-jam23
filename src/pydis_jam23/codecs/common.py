from dataclasses import dataclass


class CodecError(Exception):
    """An error encountered while trying to perform message encoding/decoding."""


@dataclass
class CodecParam:
    name: str
    type_: type[bool] | type[int] | type[str]
    default: bool | int | str

    cli_flag: str
    cli_help: str
