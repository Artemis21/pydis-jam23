from typing import Protocol

from PIL import Image

from . import lsb
from .common import CodecError

__all__ = ["CodecError", "CODECS", "Codec"]


class Codec(Protocol):
    cli_flag: str
    cli_help: str

    def encode(self, image: Image.Image, message: bytes) -> None:
        ...

    def decode(self, image: Image.Image) -> bytes:
        ...


CODECS: list[Codec] = [lsb]
