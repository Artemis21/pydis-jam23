"""Appends Data to image to display text secret on text display

Concat codec appends data to image using a custom encoding, which consists
of the XOR operator and bit-shift operator, and uses it as a storing format.
When data is retrieved/decoded then the secret code will be displayed on the
image like a scratch code thing but digital.
"""

import string
from PIL import Image, ImageDraw
from .common import CodecError

short_name = "concat"
display_name = "Concat"
cli_flag = "--concat"
cli_help = "appends encoded secret into the image"

params = []
encode_params = []
decode_params = []


buf_size = 2**8  # see which buffer size gives the faster time


class DataSect:
    start = b"START"
    end = b"END"


class BitShift:
    _min = 1
    med = 4
    _max = 7


def bit_shift_encoding(message: bytes, shift: BitShift = BitShift._min):
    msg = []
    for _byte in range(len(message)):
        msg.append(hex((message[_byte] << shift) ^ message[_byte])[2:])
    return "".join(msg)


def bit_shift_decoding(message: str, shift: BitShift = BitShift._min, charset=None):
    msg = []
    charset = list(f"{string.ascii_letters+string.digits} ".encode()) if charset is None else charset
    enc_msg = bytes.fromhex(message)
    for _byte in range(len(enc_msg)):
        for test_byte in charset:
            if (enc_msg[_byte] ^ (test_byte << shift)) in charset and (
                (test_byte << shift) ^ enc_msg[_byte]
            ) == test_byte:
                msg.append(test_byte)
    return "".join([chr(i) for i in msg])


def write_text_on_image(image: Image.Image, text: str):
    im = ImageDraw.Draw(image)
    im.text((15, 15), text)


def encode(image: Image.Image, secret: bytes, shift_level: BitShift = BitShift._min):
    data = image.tobytes()
    if data.find(DataSect.start) >= 0 and data.find(DataSect.end) >= 0:
        msg = "Image already has a secret message"
        raise CodecError(msg)
        return
    enc_msg = bit_shift_encoding(secret, shift=shift_level)
    image.putdata(DataSect.start + enc_msg.encode() + DataSect.end)
    return image


def decode(image: Image.Image, shift_level: BitShift = BitShift._min):
    image_data = image.tobytes()
    _data = []
    for i in list(image_data):
        if i != 0:
            _data.append(i)
    secret = bytearray(_data)
    secret = secret[secret.find(DataSect.start) + len(DataSect.start) : secret.find(DataSect.end)].decode()
    dec_msg = bit_shift_decoding(secret, shift=shift_level)
    write_text_on_image(image, dec_msg)
    return dec_msg.encode()
