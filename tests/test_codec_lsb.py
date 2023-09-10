import pytest
from PIL import Image
from pydis_jam23.codecs import CodecError, lsb

from .common import wikimedia_image  # noqa: F401 - import for fixtures


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
    encoded = lsb.encode(wikimedia_image, message, bits=bits, msb=msb)
    assert lsb.decode(encoded, bits=bits, msb=msb) == message


def test_message_too_long(wikimedia_image: Image.Image) -> None:
    with pytest.raises(CodecError):
        lsb.encode(wikimedia_image, bytes(1_000_000), bits=1, msb=False)
