from src.pydis_jam23.codecs.edges import encode, decode
from PIL import Image

message = "test1"
path = "/home/julian/py/.github/SummerCJ2023/pydis-jam23/tests/res/vista_de_cusco.webp"
img = Image.open(path)
encode(img,bytes(message,"utf-8"))

print(decode(img))