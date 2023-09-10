"""Encode and decode functions for the noise codec.

This codec serves as a wrapper for the standard LSB codec, but instead
of requiring a source image, it encodes your message inside a file containing
random noise.

With regular images, anyone with the original (non-encoded) image can compare
the before and after images to find the difference and decode the message by seeing
exactly which bits were changed. This is easy to do with many digital files stored
on the web. However, with random noise, there is absolutely no indication that the file
was changed, as there is no original image to compare it to.
"""
from math import ceil
from typing import Any

from numpy import random, uint8
from PIL import Image

from . import lsb

short_name = "noise"
display_name = "Noise"
cli_flag = "--noise"
cli_help = "encode your message inside random noise"


params = lsb.params
encode_params = lsb.encode_params
decode_params = lsb.decode_params


def encode(image: Image.Image, message: bytes, **codec_args: Any) -> Image.Image:  # noqa: ARG001 - use our own image
    """Encode an image into a message using our noise encoding."""
    # target bytes (noise_image must be big enough)
    num_bytes = len(message)

    # num_bytes / 3 for the 3 (RGB) channels in noise_image
    num_pixels = max(ceil(num_bytes / 3), 1024 * 768 * 3)  # at least (1024, 768) pixels

    # arbitrary 4:3 ratio
    width = int((num_pixels * 4 / 3) ** 0.5)
    height = int((num_pixels * 3 / 4) ** 0.5)

    # generate noise
    noise_array = random.randint(0, 255, (height, width, 3), dtype=uint8)
    noise_image = Image.fromarray(noise_array, "RGB")

    return lsb.encode(noise_image, message, **codec_args)


decode = lsb.decode
