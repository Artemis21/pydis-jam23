from typing import Any, Protocol, TypeVar

from PIL import Image

from . import edges, lsb
from .common import CodecError, CodecParam


class Codec(Protocol):
    short_name: str

    cli_flag: str
    cli_help: str

    params: list[CodecParam]
    encode_params: list[CodecParam]
    decode_params: list[CodecParam]

    def encode(self, image: Image.Image, message: bytes, **encode_args: Any) -> None:
        ...

    def decode(self, image: Image.Image, **decode_args: Any) -> bytes:
        ...


CODECS: list[Codec] = [lsb, edges]

__all__ = ["CodecError", "CODECS", "Codec"]
