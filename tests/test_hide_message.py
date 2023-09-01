import pathlib

import pytest
from PIL import Image
from pydis_jam23 import add_message_to_image, decode_message_from_image

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
    add_message_to_image(wikimedia_image, message)
    assert decode_message_from_image(wikimedia_image) == message
