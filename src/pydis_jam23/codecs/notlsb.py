"""Encode and decode functions for the "not" codec.

Unlike the regular LSB encoding which encodes a message within a file,
this non-serious approach takes the *image* and encodes it in another
image containing text of your secret message. In short, it does the opposite
of the standard LSB codec.
"""
import textwrap
from io import BytesIO
from math import ceil, floor
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from . import lsb
from .common import ASSETS

short_name = "not"
display_name = "Not"
cli_flag = "--not"
cli_help = "encode a file within a render of your secret message (joke encoding)"


params = lsb.params
encode_params = lsb.encode_params
decode_params = lsb.decode_params


def encode(image: Image.Image, message: bytes, **codec_args: Any) -> Image.Image:
    """Encode an image into a message using our "not" encoding."""
    # target bytes (msg_image must be big enough)
    num_bytes = len(bytearray(image.tobytes()))

    # num_bytes / 3 for the 3 (RGB) channels in msg_image
    num_pixels = max(ceil(num_bytes / 3), 1024 * 768 * 3)  # at least (1024, 768) pixels

    # arbitrary 4:3 ratio
    width = int((num_pixels * 4 / 3) ** 0.5)
    height = int((num_pixels * 3 / 4) ** 0.5)

    message = message.decode("utf-8")

    font_size = ((1000 / (len(message) ** 0.45)) + 1) or 24

    # setup draw
    msg_image = Image.new(mode="RGB", size=(width, height), color="white")
    font = ImageFont.truetype(font=str(ASSETS / "font.ttf"), size=font_size)
    draw = ImageDraw.Draw(im=msg_image)

    # wrap text
    avg_char_width = sum(font.font.getsize(char)[0][0] for char in set(message)) / len(set(message))
    max_char_count = floor((msg_image.size[0] * 0.95) / avg_char_width)
    text = textwrap.fill(text=message, width=max_char_count)

    # draw text
    draw.text(xy=(width / 2, height / 2), text=text, font=font, fill=(0, 0, 0), anchor="mm")

    image_io = BytesIO()
    image.save(image_io, format=image.format)
    image_bytes = image_io.getvalue()

    return lsb.encode(msg_image, image_bytes, **codec_args)


def decode(image: Image.Image, **codec_args: Any) -> bytes:  # noqa: ARG001
    return b"haha nice try"
