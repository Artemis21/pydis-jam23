from typing import Protocol

from PIL import Image

from . import edges, joke, lsb, lsbimage
from .common import CodecError


class Codec(Protocol):
    cli_flag: str
    cli_help: str

    def encode(self, image: Image.Image, message: bytes) -> None:
        ...

    def decode(self, image: Image.Image) -> bytes:
        ...


CODECS: list[Codec] = [edges, joke, lsb, lsbimage]

__all__ = ["CodecError", "CODECS", "Codec"]
