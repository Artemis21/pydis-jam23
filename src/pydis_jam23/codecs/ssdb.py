"""Encode and decode functions for the seed spaced data bytes codec

It works by spacing the message appart by random distances generated from 
the enterd password"""
from typing import Any
from random import seed, randint

from PIL import Image
from hashlib import sha256

from .common import CodecError, CodecParam, decode_varint, encode_varint

short_name = "ssdb"
display_name = "SSDB"
cli_flag = "--ssdb"
cli_help = "use the seed spaced data bytes codec"

params = [
    CodecParam(
        name="password",
        type_=str,
        default=None,
        required=True,
        display_name="Password",
        help_="The password used to encode/decode.",
        cli_flag="pwd",
    ),
]
encode_params = []
decode_params = []

def encode(image: Image.Image, message: bytes, **codec_args: Any) -> None:
    """Encode data by the format described above"""
    image_data = bytearray(image.tobytes())
    data = encode_varint(len(message)) + message
    password = validate_args(**codec_args)
    seed_hash = generate_seed(password) # hash the password

    if len(image_data) < len(data)*8:
        msg = "Data is to long to be encoded into this image."
        raise CodecError(msg)

    bit_stream = get_bits(data)

    byte_gen = byte_generator(image_data,seed_hash)

    for bit in bit_stream:
        location, byte = next(byte_gen)
        image_data[location] = set_lsb(byte,bit)
    
    image.frombytes(image_data)

def decode(image: Image.Image, **codec_args: Any) -> bytes:
    """Decode data by the format described above
    
    As it just reads out the data there is no check that the data is correct"""
    image_data = bytearray(image.tobytes())
    password = validate_args(**codec_args)
    seed_hash = generate_seed(password) # hash the password

    byte_gen = byte_generator(image_data,seed_hash)
    def read_next_byte() -> int:
        nonlocal byte_gen
        output_byte = []
        for _ in range(8):
            _,byte = next(byte_gen)
            output_byte.append(byte & 1)

        output = 0
        for i, bit_value in enumerate(output_byte):
            output += bit_value << i
        return output

    length = decode_varint(read_next_byte)

    message = b""
    for _ in range(length):
        message += read_next_byte().to_bytes(1,"big")

    return message

def byte_generator(image_data:bytearray,seed_hash:str)->tuple[int,bytes]:
    seed(seed_hash)
    max_step = len(image_data) - 1
    previous = []
    while True:
        random_number = randint(0,max_step)
        if random_number not in previous:
            previous.append(random_number)
            cursor = random_number
            yield cursor, image_data[cursor]

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

def generate_seed(password:str)->str:
    """Hashes the password to generate the seed"""

    hasher = sha256()
    hasher.update(password.encode("UTF-8"))
    return hasher.hexdigest()

def set_lsb(pixel: bytes, lsb_value: int) -> bytes:
    return (pixel & ~1) | lsb_value