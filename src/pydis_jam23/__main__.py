import sys

from . import cli_app, web


def main():
    if sys.argv[1:] == []:
        sys.exit(web.run_server())
    else:
        sys.exit(cli_app.run())


if __name__ == "__main__":
    main()
