"""
PYTHON CODE JAM 23
--------------------

The premise of this code is to alter the parity of RGB pixel values within
an image to encode binary data.
"""
import argparse
import sys
import typing

from PIL import Image

from src import encode_data, decode_data


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required = True)
    action.add_argument(
        "-e",
        "--encode",
        type = argparse.FileType("rb"),
        help = "An image to encode a secret message within.",
    )
    action.add_argument(
        "-d",
        "--decode",
        type = argparse.FileType("rb"),
        help = "Decodes a secret message from an image.",
    )
    args = parser.parse_args()
    if args.encode:
        encode_message(args.encode)
    else:
        decode_message(args.decode)


def encode_message(encode: typing.BinaryIO) -> None:
    message = sys.stdin.read()
    image: Image.Image = Image.open(encode)
    image = encode_data(image, message)
    image.save(sys.stdout.buffer, format = "PNG")


def decode_message(decode: typing.BinaryIO) -> None:
    image: Image.Image = Image.open(decode)
    message: str = decode_data(image)
    sys.stdout.buffer.write(message)


if __name__ == "__main__":
    main()
