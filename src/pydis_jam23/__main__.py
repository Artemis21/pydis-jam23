import sys

from . import cli_app, ui_app


def main():
    if sys.argv[1:] == []:
        sys.exit(ui_app.run())
    else:
        sys.exit(cli_app.run())


if __name__ == "__main__":
    main()
