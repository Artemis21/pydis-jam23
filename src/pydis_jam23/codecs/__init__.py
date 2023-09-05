import sys
from typing import BinaryIO, Protocol

from PIL import Image

from . import lsb
from .common import CodecError


class Codec(Protocol):
    cli_flag: str
    cli_help: str

    def encode(self, image: Image.Image, message: bytes) -> None:
        ...

    def decode(self, image: Image.Image) -> bytes:
        ...


CODECS: list[Codec] = [lsb]


def encode_message(plain: BinaryIO, codec: Codec, gui_data: str | None = None) -> None:
    if gui_data is None:
        message = sys.stdin.buffer.read()
        image = Image.open(plain)
        codec.encode(image, message)
        image.save(sys.stdout.buffer, format="PNG")
    else:
        message = gui_data.encode("utf-8")  # ui_app message
        image = Image.open(plain)
        codec.encode(image, message)
        return image


def decode_message(extract: BinaryIO, codec: Codec, gui_data: str | None = None) -> None:
    if gui_data is None:
        image = Image.open(extract)
        message = codec.decode(image)
        sys.stdout.buffer.write(message)
    else:
        image = Image.open(gui_data)  # image file
        message = codec.decode(image)
        return message


__all__ = ["CodecError", "CODECS", "Codec", "encode_message", "decode_message"]
