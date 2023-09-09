import pathlib

import pytest
from PIL import Image

RES_DIR = pathlib.Path(__file__).parent / "res"


@pytest.fixture
def wikimedia_image() -> Image.Image:
    return Image.open(RES_DIR / "vista_de_cusco.webp")
