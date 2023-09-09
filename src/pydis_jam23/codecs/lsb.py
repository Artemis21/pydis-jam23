"""Encode and decode functions for the LSB codec.

This codec stores your message in the least significant bit of each byte of
image data. This means that a typical RGB image has space for three bits of
data per pixel. Your message will be prefixed with its length, itself encoded
using a variable length encoding to avoid a large section of zeros at the start
of the message giving it away.
"""
from PIL import Image

from .common import CodecError, read_bytes_from_image, int_to_bytes, bytes_to_int

cli_flag = "--lsb"
cli_help = "use the least significant bit codec"

def encode(image: Image.Image, data: bytes) -> None:
    """Encode a message into an image using our LSB encoding."""
    length = int_to_bytes(len(data))
    data = length + data
    bytes_data = bytearray(image.tobytes())

    if len(data) * 8 > len(bytes_data):
        msg = "Data is too long to fit in image."
        raise CodecError(msg)

    for byte_idx, message_byte in enumerate(data):
        base_bit_idx = byte_idx * 8

        for bit_offset in range(8):
            bit_idx = base_bit_idx + bit_offset
            pixel = bytes_data[bit_idx] & 0b1111_1110
            flag = (message_byte >> bit_offset) & 1
            bytes_data[bit_idx] = pixel | flag

    image.frombytes(bytes_data)

def decode(image: Image.Image) -> bytes:
    """Decode a message from an image using our LSB encoding."""
    data = bytes(image.tobytes())
    offset = 0

    def read_next_byte() -> int:
        nonlocal offset
        byte = read_bytes_from_image(data, offset, 1)
        offset += 8
        return byte[0]

    length = bytes_to_int(read_next_byte)

    return read_bytes_from_image(data, offset, length)
