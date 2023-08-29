# Readable Regexes

Once we've worked out what our project is, this file should describe it. For now, here are some instructions on setting the project up.

## Installation

This project uses [Hatch](https://hatch.pypa.io) for dependency management and virtual environments. Hatch can be installed with `pip install hatch` among [other methods](https://hatch.pypa.io/latest/install/).

You'll also need to clone this repository locally, which you can do with `git clone https://github.com/Artemis21/pydis-jam23`. Finally, `cd` into the project directory and run `hatch run hooks` to install pre-commit linting hooks.

Other commands you can run through hatch include:
- `hatch run lint`: Run linting checks, which tell you when there are style issues in your code.
- `hatch run fmt`: Run code formatting to automatically enforce style consistency.
- `hatch run main`: Runs the project code itself.
