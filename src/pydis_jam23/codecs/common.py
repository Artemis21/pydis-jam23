import pathlib
from collections.abc import Callable
from dataclasses import dataclass


class CodecError(Exception):
    """An error encountered while trying to perform message encoding/decoding."""


@dataclass
class CodecParam:
    name: str
    type_: type[bool] | type[int] | type[str]
    default: bool | int | str | None
    required: bool

    display_name: str
    help_: str
    cli_flag: str


ASSETS = pathlib.Path(__file__).parent.parent / "assets"
SEVEN_BIT_MAX = 127


def encode_varint(value: int) -> bytes:
    """Encode an integer using a variable length encoding.

    Specifically, the most significant bit of each byte is used to indicate
    whether or not it is the last byte in the encoding. The remaining seven
    bits are used to store the value, in little-endian order.
    """
    encoded = bytearray()
    while value > SEVEN_BIT_MAX:
        encoded.append(0b1000_0000 | (value & 0b0111_1111))
        value >>= 7
    encoded.append(value)
    return bytes(encoded)


def decode_varint(read_byte: Callable[[], int]) -> int:
    """Decode a variable length integer given a function to read the next byte."""
    value = 0
    shift = 0
    while True:
        byte = read_byte()
        value |= (byte & 0b0111_1111) << shift
        if byte & 0b1000_0000 == 0:
            break
        shift += 7
    return value
