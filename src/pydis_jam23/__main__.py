import argparse
import sys
import typing

from PIL import Image

from pydis_jam23 import add_message_to_image, decode_message_from_image


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "-p",
        "--plain",
        type=argparse.FileType("rb"),
        help="A plain image to hide a message from stdin in, writes PNG to stdout",
    )
    action.add_argument(
        "-x",
        "--extract",
        type=argparse.FileType("rb"),
        help="Extract a message from an image to stdout",
    )
    args = parser.parse_args()
    if args.plain:
        encode_message(args.plain)
    else:
        decode_message(args.extract)


def encode_message(plain: typing.BinaryIO) -> None:
    message = sys.stdin.read()
    image = Image.open(plain)
    add_message_to_image(image, message.encode())
    image.save(sys.stdout.buffer, format="PNG")


def decode_message(extract: typing.BinaryIO) -> None:
    image = Image.open(extract)
    message = decode_message_from_image(image)
    sys.stdout.buffer.write(message)


if __name__ == "__main__":
    main()
