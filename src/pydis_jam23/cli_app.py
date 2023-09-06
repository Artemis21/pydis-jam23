import argparse
import sys
import typing

from PIL import Image

from .codecs import CODECS, Codec, CodecError


def run():
    args = build_arg_parser().parse_args()
    try:
        if args.plain:
            encode_message(args.plain, args.codec)
        else:
            decode_message(args.extract, args.codec)
    except CodecError as e:
        if args.verbose > 0:
            raise
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity")
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
    return parser


def encode_message(plain: typing.BinaryIO, codec: Codec) -> None:
    message = sys.stdin.buffer.read()
    image = Image.open(plain)
    codec.encode(image, message)
    image.save(sys.stdout.buffer, format="PNG")


def decode_message(extract: typing.BinaryIO, codec: Codec) -> None:
    image = Image.open(extract)
    message = codec.decode(image)
    sys.stdout.buffer.write(message)
