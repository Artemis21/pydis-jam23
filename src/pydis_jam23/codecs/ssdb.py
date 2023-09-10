"""Encode and decode functions for the seed spaced data bytes codec

It works by spacing the message appart by random distances generated from 
the enterd password"""
from typing import Any
from random import seed, randint

from PIL import Image
from hashlib import sha256

from .common import CodecError, CodecParam, decode_varint, encode_varint

short_name = "ssdb"
cli_flag = "--ssdb"
cli_help = "use the seed spaced data bytes codec"

params = [
    CodecParam(
        name="password",
        type_=str,
        default=None,
        cli_flag="pwd",
        cli_help="The password used to encode/decode.",
    ),
]
encode_params = []
decode_params = []

def encode(image: Image.Image, message: bytes, **codec_args: Any) -> None:
    image_data = image.tobytes()
    data = encode_varint(len(message)) + message
    password = validate_args(**codec_args)
    seed_hash = generate_seed(password)
    if len(image_data) < len(data):
        msg = "Data is to big to be encoded into this image."
        raise CodecError(msg)

    bit_stream = get_bits(data)

    seed(seed_hash) # set the random number generator to the set seed

    

def decode(image: Image.Image, **codec_args: Any) -> bytes:
    pass

def validate_args(**kwargs: Any)->str:
    """Validate the arguments passed to the codec."""
    password = kwargs.pop("password")
    if kwargs:
        msg = f"Unexpected arguments: {', '.join(kwargs)}"
        raise TypeError(msg)
    if password is None:
        msg = "A password is required."
        raise CodecError(msg)
    return password

def get_bits(data:bytes)->list[int]:
    """Converst bynary data into a list of 0 | 1"""
    data_binary = []
    for byte in data:
        for bit_idx in range(8):
            data_binary.append((byte >> bit_idx) & 1)
    return data_binary

def generate_seed(password:str)->int:
    """Hashes the password to generate the seed"""

    hasher = sha256()
    hasher.update(password.encode("UTF-8"))
    return hasher.hexdigest()


def set_lsb(pixel: bytes, lsb_value: int) -> bytes:
    return (pixel & ~1) | lsb_value