"""Encode image and decode image functions for the joke-LSB codec.
"""
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont

from .lsbimage import encode_image, decode_image

cli_flag = "--lsb-joke"
cli_help = "use the least significant bit codec (joke)"

def joke_encode(image: Image.Image, message: bytes) -> None:
    """Encode an image into a message using our joke-LSB encoding."""
    num_bytes = len(bytearray(image.tobytes()))
    num_pixels = max(math.ceil(num_bytes / 3), 1024 * 768 * 3) # at least (1024, 768) pixels
    width = int((num_pixels * 4 / 3) ** 0.5)
    height = int((num_pixels * 3 / 4) ** 0.5)

    message = message.decode("utf-8")
    font_size = ((1000 / (len(message) ** 0.45)) + 1) or 24

    msg_image = Image.new(mode = "RGB", size = (width, height), color = "white")
    font = ImageFont.truetype(font = "../assests/font.ttf", size = font_size)
    draw = ImageDraw.Draw(im = msg_image)

    avg_char_width = sum(font.font.getsize(char)[0][0] for char in set(message)) / len(set(message))
    max_char_count = math.floor((msg_image.size[0] * 0.95) / avg_char_width)
    scaled_wrapped_text = textwrap.fill(text = message, width = max_char_count)

    draw.text(xy = (width / 2, height / 2), text = scaled_wrapped_text, font = font, fill = (0, 0, 0), anchor="mm")
    encode_image(msg_image, image)

def joke_decode(image: Image.Image) -> Image.Image:
    """Decode an image from a message using our joke-LSB encoding."""
    return decode_image(image)
