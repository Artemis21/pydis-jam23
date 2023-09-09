"""Encode a message into the given image.
using as custom LSB variant

One of the color channels is randomly seclected.
On this channel edge detection is run.
The pixels that are detected as edges will then be used,
by to store data in the other two channels.

Which channels is used is marked on the 0,0 pixel.
Channel with a 1 as LSB is the mask
"""
from random import randint

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

from .common import CodecError, decode_varint, encode_varint

cli_flag = "--edges"
cli_help = "use the edges codec"

# ruff: noqa: PLR2004
def encode(image: Image.Image, message: bytes) -> None:
    """encode a message into an image using the above described method"""
    image_data = bytearray(image.tobytes())
    data = encode_varint(len(message)) + message

    mask_color = randint(0, 2)  # noqa S311
    # idk just random cus more fun
    alternative_trys = 0

    # check if the channels is big enugh for the message
    # try the other ones if not
    while True:
        edges = get_edges(image.split()[mask_color]).tobytes()
        if count_color(edges, 0) > len(data):  # count edge pixels
            break
        elif alternative_trys >= 2:
            msg = "The message is to long to be encoded into this image."
            raise CodecError(msg)
        alternative_trys += 1
        mask_color = (mask_color + alternative_trys) % 3

    for idx in range(0, 3):  # set all LSB of the first image to 0
        image_data[idx] = set_lsb(image_data[idx], 0)

    # set the LSB of the color that is used as information mask to 1
    image_data[mask_color] = set_lsb(image_data[mask_color], 1)

    # get data spaces at index 1 -> as index 0 (pixel 0,0) marks the color layer used as mask
    data_indices = generate_data_indeces(edges, mask_color, len(data) * 8, 1)

    # split bytes to bits
    message_binary = []
    for byte in data:
        for bit_idx in range(8):
            message_binary.append((byte >> bit_idx) & 1)

    # modify the image
    for bit_idx, pixel_idx in enumerate(data_indices):
        image_data[pixel_idx] = set_lsb(image_data[pixel_idx], message_binary[bit_idx])

    image.frombytes(image_data)


def decode(image: Image.Image) -> bytes:
    data = image.tobytes()

    # get the layer wich is used as the mask
    mask_color = None
    for channel in range(0, 3):  # bytes 0-2 are have the RGB values of pixel 0,0
        if bool(data[channel] % 2):  # get the value of the LSB of the channel
            if mask_color is None:
                mask_color = channel
            else:
                msg = "Wrong codec, corrupted file or no encoded data."
                raise CodecError(msg)

    if mask_color is None:
        msg = "Wrong codec, corrupted file or no encoded data."
        raise CodecError(msg)

    # generate the mask that was used to encode the data
    edges = get_edges(image.split()[mask_color]).tobytes()

    offset = 1

    def wrapper_for_next_byte() -> int:
        nonlocal offset
        byte, new_offset = read_next_byte(edges, data, mask_color, offset)
        offset = new_offset
        return byte[0]

    length = decode_varint(wrapper_for_next_byte)

    # finally load message
    message = b""
    for _ in range(length):
        new_byte, new_offset = read_next_byte(edges, data, mask_color, offset)
        offset = new_offset
        message += new_byte

    return message


def count_color(image: bytes, color: int | tuple[int, int, int]) -> int:
    """Count the how many pixels have a color in an image"""

    count = 0
    for pixel in image:
        if pixel == color:
            count += 1
    return count


def read_next_byte(edges: bytes, image_data: bytes, mask_color: int, pixel_index_offset: int) -> tuple[bytes, int]:
    """Read the next byte of data out of an image while accounting for the edges mask

    :param edges: The raw byte data of the edges mask 0 -> Edge
    :param image_data: Raw data of the image 3 Bytes per pixel RGB
    :param mask_color: The index of wich channel is represented by edges 0-R 1-G 2-B
    :param pixel_index_offset: the index of the pixel on wich the function starts searching
    :return: tuple, the data of the byte and the pixel it has stopped on
    :raises: Codec error when no data is found"""
    output_byte = []

    pixel_index = pixel_index_offset
    color_offset = 0

    # stop when 8 bit are found
    while len(output_byte) < 8:
        # skip when the pixels is no data pixel
        if edges[pixel_index] == 0:
            # convert pixel index to image index which is in RGB so 3 byte per pixel
            pixel_start = pixel_index * 3

            # read both channels that are not part of the mask
            if color_offset != mask_color:
                # %2 is used to get the LSB
                output_byte.append(image_data[pixel_start + color_offset] % 2)
            color_offset += 1

            # if done with the pixel move on the next
            if color_offset > 2:
                pixel_index += 1
                color_offset = 0

        else:
            pixel_index += 1

        # if we are looking at pixels outside the image no data was found
        if pixel_index > len(edges):
            msg = "Image contains no data or is corrupted."
            raise CodecError(msg)

    output = 0
    for i, bit_value in enumerate(output_byte):
        output += bit_value * (2**i)

    return output.to_bytes(1, "big"), pixel_index


def set_lsb(pixel: bytes, lsb_value: int) -> bytes:
    return (pixel & ~1) | lsb_value


def generate_data_indeces(edges: bytes, mask_color: int, message_length: int, start_byte: int) -> list[int]:
    """Generate The indeces in the bytearray of the image where the data will
    be located

    :param edges: raw data of the edge mask 0-> Edge
    :param mask_color: The index of wich channel is represented by edges 0-R 1-G 2-B
    :param message_length: the amount of bits the data will contain
    :param start_byte: the index in edges where the search will begin
    :return: a list of indexs for the original image in wich the data will be encoded its length == message_length
    """
    pixel_index = start_byte
    data_indices = []
    offset_index = 0

    # only create value until message_length is reached
    while len(data_indices) < message_length:
        # if the pixels is black in the mask, use it for data
        if edges[pixel_index] == 0:
            # tranfer between greayscale an rgb
            first_in_pixel = pixel_index * 3

            # ensure that data is only saved on the non mask color layer
            if offset_index != mask_color:
                data_indices.append(first_in_pixel + offset_index)
            offset_index += 1

            # only go to next pixel if both channels have been filled
            if offset_index > 2:
                pixel_index += 1
                offset_index = 0
        else:
            # skip the pixels
            pixel_index += 1

    return data_indices


def get_edges(image: Image.Image) -> Image.Image:
    """Find the Edges in an Image and mark them
    - black pixels mark edges"""

    # get the edges
    contours = image.filter(ImageFilter.CONTOUR)

    # increase saturation to increase difference between noise and actual adges
    enhancer = ImageEnhance.Contrast(contours)
    high_contrast = enhancer.enhance(15)

    # filter out the noise
    cleand = high_contrast.filter(ImageFilter.MedianFilter)

    # make image binary
    black_white = cleand.convert("1")

    # remove the outline that runs around the entire image
    drawer = ImageDraw.Draw(black_white)
    drawer.rectangle([0, 0, image.width - 1, image.height - 1], fill=None, outline=1, width=1)

    # make it greayscale again because its easyer to iterate over bytes then bits
    return black_white.convert("L")
