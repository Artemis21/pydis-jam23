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
@pytest.mark.parametrize("bits", [1, 3, 8])
@pytest.mark.parametrize("msb", [False, True])
def test_message_roundtrip(wikimedia_image: Image.Image, message: bytes, bits: int, msb: bool) -> None:
    lsb.encode(wikimedia_image, message, bits=bits, msb=msb)
    assert lsb.decode(wikimedia_image, bits=bits, msb=msb) == message


def test_message_too_long(wikimedia_image: Image.Image) -> None:
    with pytest.raises(CodecError):
        lsb.encode(wikimedia_image, bytes(1_000_000), bits=1, msb=False)
