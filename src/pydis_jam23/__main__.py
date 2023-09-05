import argparse
import sys

from .codecs import CODECS, CodecError, decode_message, encode_message

# from . import
from .ui_app import run_app


def run_cli():
    args = build_arg_parser().parse_args()
    # print( CODECS[0] )
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


def main():
    if sys.argv[1:] == []:
        sys.exit(run_app())
    else:
        sys.exit(run_cli())


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    # print( parser.parse_args() )
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


if __name__ == "__main__":
    main()
