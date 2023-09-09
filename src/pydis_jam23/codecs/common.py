"""Shared functions between codecs
"""

from collections.abc import Callable

SEVEN_BIT_MAX = 127

class CodecError(Exception):
    """An error encountered while trying to perform message encoding/decoding."""


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


def int_to_bytes(value: int) -> bytes:
    """Encode an integer using a variable length encoding.

    Specifically, the most significant bit of each byte is used to indicate
    whether or not it is the last byte in the encoding. The remaining seven
    bits are used to store the value, in little-endian order.
    """
    encoded = bytearray()

    while value > SEVEN_BIT_MAX:
        encoded.append(0b1000_0000 | (value & 0b0111_1111))
        value >>= 7

    encoded.append(value)

    return bytes(encoded)

def bytes_to_int(read_byte: Callable[[], int]) -> int:
    """Decode a variable length integer given a function to read the next byte."""
    value = 0
    shift = 0

    while True:
        byte = read_byte()
        value |= (byte & 0b0111_1111) << shift

        if byte & 0b1000_0000 == 0:
            break

        shift += 7

    return value
