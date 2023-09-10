import string
import sys

from PIL import Image, ImageDraw, ImageFont

buf_size = 2**8  # see which buffer size gives the faster time


class SeekMode:
    _set = 0
    cur = 1
    end = 2


class DataSect:
    start = b"start\x00\x00\x00\x00"
    end = b"\x00\x00\x00\x00END"


class BitShift:
    _min = 1
    med = 4
    _max = 7


def get_file_size(file_handler):
    file_size = file_handler.seek(0, SeekMode.end)
    file_handler.seek(file_size * -1, SeekMode.cur)
    return file_size


def get_from_image(pathtoimage):
    # gets secret in image
    with open(pathtoimage, "rb") as image_file:
        buf_to_read = get_file_size(image_file)

        buf_sect = 1
        cumulative_buf = []
        _continue = False
        key = len(DataSect.start) - 1
        secret_start = None

        while True:
            sector = buf_to_read - (buf_size * buf_sect) if buf_to_read > (buf_size * buf_sect) else 0

            image_file.seek(sector, SeekMode._set)
            try:
                data = image_file.read(buf_size)
            except OverflowError:
                print(f'"{buf_size}" Buffer is to big')
                sys.exit()

            try:
                if DataSect.start[key] in data and _continue is True:
                    cumulative_buf.append(data)
                    key = key - buf_size if key >= 0 else -1
                    secret_start = buf_size * (buf_sect - 1)
                elif _continue is True:
                    cumulative_buf = []
            except IndexError:
                break

            if _continue is False:
                cumulative_buf.append(data)
                if DataSect.end in b"".join(cumulative_buf[::-1]):
                    # print( 'secret data is available in image' )
                    cumulative_buf = []
                    _continue = True

            buf_sect += 1
            if sector == 0:
                break

        if secret_start:
            image_file.seek(buf_to_read - secret_start, SeekMode._set)
            data = image_file.read()
            return data[data.find(DataSect.start) + len(DataSect.start) : -len(DataSect.end)]
        else:
            return None


def put_into_image(pathtoimage: str, newimagename: str, secret: bytes):
    # puts secret in image
    new_image = open(newimagename, "wb")

    with open(pathtoimage, "rb") as image_file:
        buf_to_read = get_file_size(image_file)

        _eof = False
        buf_sect = 1

        while not _eof:
            data = image_file.read(buf_size)
            image_file.seek(buf_size * buf_sect, SeekMode._set)
            buf_to_read -= buf_size
            new_image.write(data)
            if buf_to_read < len(data):
                _eof = True
                data = image_file.read() + DataSect.start + secret + DataSect.end
                new_image.write(data)
            buf_sect += 1

    new_image.close()


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


def write_text_on_image(image: Image.Image, text: str, output_file: str, fontsize=10):
    im = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", fontsize)
    im.text((15, 15), text, font=font)
    image.save(output_file)


def show_concat_secret(
    image_path: str, output_file: str, custom_charset: str | None = None, shift_level: BitShift = None
):
    charset = list(custom_charset) if custom_charset is not None else f"{string.ascii_letters} {string.digits}".encode()
    shift_level = shift_level if shift_level is not None else BitShift._min
    secret = get_from_image(image_path).decode()
    if secret:
        dec_msg = bit_shift_decoding(secret, shift=shift_level, charset=charset)
        write_text_on_image(Image.open(image_path), dec_msg, output_file)
    else:
        print("Image has no secret")


def hide_concat_secret(image_path: str, secret: str, output_file: str):
    enc_msg = bit_shift_encoding(secret.encode(), BitShift._min)
    if get_from_image(image_path) is None:
        put_into_image(image_path, output_file, enc_msg.encode())
    else:
        print("Image already has a secret message")


# hide_concat_secret( '../../../image.jpg', 'this is some secret CODE 1', 'image1.jpg' )
# show_concat_secret( 'image1.jpg', 'image_out.jpg' )
