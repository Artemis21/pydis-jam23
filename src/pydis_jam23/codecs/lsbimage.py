"""Encode image and decode image functions for the LSB codec.
"""
from io import BytesIO
from PIL import Image

from .lsb import encode, decode

cli_flag = "--lsb-image"
cli_help = "use the least significant bit codec (images)"

def encode_image(image: Image.Image, image2: Image.Image) -> None:
    """Encode an image into another image using our LSB encoding."""
    image_io = BytesIO()
    image2.save(image_io, format=image2.format)
    image2_bytes = image_io.getvalue()
    encode(image, image2_bytes)

def decode_image(image: Image.Image) -> Image.Image:
    """Decode an image from another image using our LSB encoding."""
    image2_bytes = decode(image)
    image_io = BytesIO(image2_bytes)
    image_io.seek(0)
    return Image.open(image_io)
