import pytest
from PIL import Image
from pydis_jam23.codecs import CodecError, edges

from .common import wikimedia_image  # noqa: F401 - import for fixtures


@pytest.mark.parametrize(
    "message",
    [
        b"",
        b"Hello, world!",
        bytes(range(256)),
    ],
)
@pytest.mark.parametrize("mask_color", [0, 1, 2])
def test_message_roundtrip(wikimedia_image: Image.Image, message: bytes, mask_color: int) -> None:
    encoded = edges.encode(wikimedia_image, message, test_channel=mask_color)
    assert edges.decode(encoded) == message


def test_message_too_long(wikimedia_image: Image.Image) -> None:
    with pytest.raises(CodecError):
        edges.encode(wikimedia_image, bytes(1_000_000))
