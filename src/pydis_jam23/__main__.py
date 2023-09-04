import argparse
import sys
import typing

from PIL import Image

from .codecs import CODECS, Codec


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "-p",
        "--plain",
        metavar="FILE",
        type=argparse.FileType("rb"),
        help="a plain image to hide a message from stdin in, writes PNG to stdout",
    )
    action.add_argument(
        "-x",
        "--extract",
        metavar="FILE",
        type=argparse.FileType("rb"),
        help="extract a message from an image to stdout",
    )
    codec_arg = parser.add_mutually_exclusive_group(required=True)
    for codec in CODECS:
        codec_arg.add_argument(
            codec.cli_flag,
            action="store_const",
            const=codec,
            dest="codec",
            help=codec.cli_help,
        )
    args = parser.parse_args()
    if args.plain:
        encode_message(args.plain, args.codec)
    else:
        decode_message(args.extract, args.codec)


def encode_message(plain: typing.BinaryIO, codec: Codec) -> None:
    message = sys.stdin.read()
    image = Image.open(plain)
    codec.encode(image, message.encode())
    image.save(sys.stdout.buffer, format="PNG")


def decode_message(extract: typing.BinaryIO, codec: Codec) -> None:
    image = Image.open(extract)
    message = codec.decode(image)
    sys.stdout.buffer.write(message)


if __name__ == "__main__":
    main()
