"""Encode and decode functions for the LSB codec.

This codec stores your message in the least significant bit of each byte of
image data. This means that a typical RGB image has space for three bits of
data per pixel. Your message will be prefixed with its length, itself encoded
using a variable length encoding to avoid a large section of zeros at the start
of the message giving it away.
"""
from collections.abc import Iterator
from typing import Any

from PIL import Image

from .common import CodecError, CodecParam, decode_varint, encode_varint

short_name = "lsb"
display_name = "LSB"
cli_flag = "--lsb"
cli_help = "use the least significant bits codec"

params = [
    CodecParam(
        name="bits",
        type_=int,
        default=1,
        required=False,
        display_name="Bits",
        help_="number of bits to store per pixel",
        cli_flag="bits",
    ),
    CodecParam(
        name="msb",
        type_=bool,
        default=False,
        required=False,
        display_name="MSB",
        help_="use the most significant bits instead",
        cli_flag="msb",
    ),
]
encode_params = []
decode_params = []


def encode(image: Image.Image, message: bytes, **codec_args: Any) -> Image.Image:
    """Encode a message into an image using our LSB encoding."""
    bits, msb = validate_args(**codec_args)
    if bits < 1 or bits > 8:
        msg = "Bit count must be between 1 and 8."
        raise CodecError(msg)
    length = encode_varint(len(message))
    message = length + message
    data = bytearray(image.tobytes())
    if len(message) * 8 > len(data) * bits:
        msg = "Message is too long to fit in image."
        raise CodecError(msg)
    for bit_idx, data_bit in enumerate(iterate_bits(message)):
        pixel_idx, pixel_bit = divmod(bit_idx, bits)
        shift = (7 - pixel_bit) if msb else pixel_bit
        mask = ~(1 << shift)
        pixel = data[pixel_idx] & mask  # clear the bit
        pixel |= data_bit << shift  # set the bit
        data[pixel_idx] = pixel
    return Image.frombytes(image.mode, image.size, data)


def decode(image: Image.Image, **codec_args: Any) -> bytes:
    """Decode a message from an image using our LSB encoding."""
    bits, msb = validate_args(**codec_args)
    data = bytes(image.tobytes())
    offset = 0

    def read_next_byte() -> int:
        nonlocal offset
        byte = read_bytes_from_image(data, offset, length=1, bits_per_pixel=bits, msb=msb)
        offset += 8
        return byte[0]

    length = decode_varint(read_next_byte)
    return read_bytes_from_image(data, offset, length, bits, msb)


def validate_args(**kwargs: Any) -> tuple[int, bool]:
    """Validate the arguments passed to the codec."""
    bits = kwargs.pop("bits")
    msb = kwargs.pop("msb")
    if kwargs:
        msg = f"Unexpected arguments: {', '.join(kwargs)}"
        raise TypeError(msg)
    if bits < 1 or bits > 8:
        msg = "Bit count must be between 1 and 8."
        raise CodecError(msg)
    return bits, msb


def iterate_bits(data: bytes) -> Iterator[int]:
    """Iterate over the bits in a byte string."""
    for byte in data:
        for bit_idx in range(8):
            yield (byte >> bit_idx) & 1


def read_bytes_from_image(image_data: bytes, offset: int, length: int, bits_per_pixel: int, msb: bool) -> bytes:
    """Read a number of bytes from an image, starting at a given offset.

    :param image_bytes: The raw bytes of the image to read from.
    :param offset: The number of bits to skip before reading.
    :param length: The number of bytes to read.
    :param bits_per_pixel: The number of bits containing data per pixel.
    :param msb: Whether to read the most significant bits instead of the least.
    :return: The bytes read from the image.
    :raises ValueError: If the message data would exceed the size of the image.
    """
    if (offset + length * 8) > len(image_data) * bits_per_pixel:
        msg = "Image does not contain a message."
        raise CodecError(msg)
    message = bytearray()
    for bit_idx in range(offset, offset + length * 8):
        local_bit_idx = bit_idx & 0b111
        if local_bit_idx == 0:
            message.append(0)
        pixel_idx, pixel_bit = divmod(bit_idx, bits_per_pixel)
        shift = (7 - pixel_bit) if msb else pixel_bit
        data_bit = (image_data[pixel_idx] >> shift) & 1
        message[-1] |= data_bit << local_bit_idx
    return bytes(message)
