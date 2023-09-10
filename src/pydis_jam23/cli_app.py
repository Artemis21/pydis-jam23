import argparse
import sys
import typing

from PIL import Image

from .codecs import CODECS, Codec, CodecError, CodecParam


def run():
    args = build_arg_parser().parse_args()
    codec: Codec = args.codec
    params = codec.params + (codec.encode_params if args.plain else codec.decode_params)
    extra_args = find_args(args, codec, params)
    try:
        if args.plain:
            encode_message(args.plain, codec, extra_args)
        else:
            decode_message(args.extract, codec, extra_args)
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
        for param in codec.params:
            add_codec_arg(parser, codec, param, when="codec")
        for param in codec.encode_params:
            add_codec_arg(parser, codec, param, when="encode")
        for param in codec.decode_params:
            add_codec_arg(parser, codec, param, when="decode")
    return parser


def add_codec_arg(parser: argparse.ArgumentParser, codec: Codec, param: CodecParam, when: str) -> None:
    settings: dict[str, typing.Any]
    if issubclass(param.type_, bool):
        settings = {"action": "store_true"}
    elif issubclass(param.type_, int | str):
        settings = {"metavar": param.cli_flag.upper(), "type": param.type_}
    else:
        msg = f"Unknown arg type {param.type_}"
        raise TypeError(msg)
    parser.add_argument(
        f"{codec.cli_flag}-{param.cli_flag}",
        help=f"[{codec.short_name} {when}] {param.help_}",
        default=param.default,
        dest=codec_arg_qualname(codec, param),
        **settings,
    )


def find_args(all_args: argparse.Namespace, codec: Codec, params: list[CodecParam]) -> dict[str, typing.Any]:
    args: dict[str, typing.Any] = {}
    for param in params:
        arg = getattr(all_args, codec_arg_qualname(codec, param))
        if arg in (None, "") and param.required:
            msg = f"{codec.display_name} codec requires {codec.cli_flag}-{param.cli_flag} to be given."
            print(msg, file=sys.stderr)
            sys.exit(1)
        args[param.name] = arg
    return args


def codec_arg_qualname(codec: Codec, param: CodecParam) -> str:
    return f"codec-{codec.short_name}-{param.name}"


def encode_message(plain: typing.BinaryIO, codec: Codec, extra_args: dict[str, typing.Any]) -> None:
    message = sys.stdin.buffer.read()
    image = Image.open(plain)
    image = codec.encode(image, message, **extra_args)
    image.save(sys.stdout.buffer, format="PNG")


def decode_message(extract: typing.BinaryIO, codec: Codec, extra_args: dict[str, typing.Any]) -> None:
    image = Image.open(extract)
    message = codec.decode(image, **extra_args)
    sys.stdout.buffer.write(message)
