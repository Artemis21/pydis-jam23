import pathlib

import pytest
from PIL import Image

from pydis_jam23.codecs import CodecError, lsb

RES_DIR = pathlib.Path(__file__).parent / "res"


@pytest.fixture
def wikimedia_image() -> Image.Image:
    return Image.open(RES_DIR / "vista_de_cusco.webp")


@pytest.mark.parametrize(
    "message",
    [
        b"",
        b"Hello, world!",
        bytes(range(256)),
    ],
)
def test_message_roundtrip(wikimedia_image: Image.Image, message: bytes) -> None:
    lsb.encode(wikimedia_image, message)
    assert lsb.decode(wikimedia_image) == message


def test_message_too_long(wikimedia_image: Image.Image) -> None:
    with pytest.raises(CodecError):
        lsb.encode(wikimedia_image, bytes(1_000_000))
