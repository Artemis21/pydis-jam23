"""Encode and decode functions for the LSB codec.

This codec stores your message in the least significant bit of each byte of
image data. This means that a typical RGB image has space for three bits of
data per pixel. Your message will be prefixed with its length, itself encoded
using a variable length encoding to avoid a large section of zeros at the start
of the message giving it away.
"""
from collections.abc import Callable

from PIL import Image

from .common import CodecError, decode_varint, encode_varint

cli_flag = "--lsb"
cli_help = "use the least significant bit codec"


def encode(image: Image.Image, message: bytes) -> None:
    """Encode a message into an image using our LSB encoding."""
    length = encode_varint(len(message))
    message = length + message
    data = bytearray(image.tobytes())
    if len(message) * 8 > len(data):
        msg = "Message is too long to fit in image."
        raise CodecError(msg)
    for byte_idx, message_byte in enumerate(message):
        base_bit_idx = byte_idx * 8
        for bit_offset in range(8):
            bit_idx = base_bit_idx + bit_offset
            pixel = data[bit_idx] & 0b1111_1110
            flag = (message_byte >> bit_offset) & 1
            data[bit_idx] = pixel | flag
    image.frombytes(data)


def decode(image: Image.Image) -> bytes:
    """Decode a message from an image using our LSB encoding."""
    data = bytes(image.tobytes())
    offset = 0

    def read_next_byte() -> int:
        nonlocal offset
        byte = read_bytes_from_image(data, offset, 1)
        offset += 8
        return byte[0]

    length = decode_varint(read_next_byte)
    return read_bytes_from_image(data, offset, length)


def read_bytes_from_image(image_data: bytes, offset: int, length: int) -> bytes:
    """Read a number of bytes from an image, starting at a given offset.

    :param image_bytes: The raw bytes of the image to read from.
    :param offset: The number of pixels to skip before reading.
    :param length: The number of bytes to read.
    :return: The bytes read from the image.
    :raises ValueError: If the message data would exceed the size of the image.
    """
    if (offset + length * 8) > len(image_data):
        msg = "Image does not contain a message."
        raise CodecError(msg)
    message = bytearray()
    for bit_idx in range(offset, offset + length * 8):
        local_bit_idx = bit_idx & 0b111
        if local_bit_idx == 0:
            message.append(0)
        message[-1] |= (image_data[bit_idx] & 1) << local_bit_idx
    return bytes(message)