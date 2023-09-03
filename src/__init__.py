
from PIL import Image


def _str_to_binary_tuples(message: str) -> list[tuple[int, int, int]]:
    """Convert a string toa binary array."""
    binary_array: list[tuple[int, int, int]] = []
    num_bytes = 0

    for char in message:
        char_binary: str = bin(ord(char))[2:]
        char_binary_padded: str = '0' * (-len(char_binary) % 8) + char_binary
        char_bytes: list[str] = [char_binary_padded[i:i+8] for i in range(0, len(char_binary_padded), 8)]
        num_bytes += len(char_bytes)

        for index, byte in enumerate(char_bytes):
            # first bit indicates whether it is a new character or a continuation
            # of the same character (1 = new char, 0 = same char)
            byte = ('1' if index == 0 else '0') + byte
            bits = [tuple(map(int, byte[i:i+3])) for i in range(0, len(byte), 3)]

            for bit in bits:
                binary_array.append(bit)

    # encode byte count using similar logic
    bytes_binary: str = bin(num_bytes)[2:]
    bytes_binary_padded: str = '0' * (-len(bytes_binary) % 8) + bytes_binary
    # naming leaves something to be desired
    bytes_bytes: list[str] = [bytes_binary_padded[i:i+8] for i in range(0, len(bytes_binary_padded), 8)]

    for index, byte in enumerate(bytes_bytes):
        byte: str = ('1' if index == 0 else '0') + byte
        bits: list[tuple[int, ...]] = [tuple(map(int, byte[i:i+3])) for i in range(0, len(byte), 3)]

        for bit_index, bit in enumerate(bits):
            binary_array.insert((index + bit_index), bit)

    print(binary_array)

    return binary_array


def encode_data(image: Image.Image, message: str, out_path: str = None) -> Image.Image:
    """Encodes a string within an image."""
    encoded_image: Image.Image = _encode_data(image, message)

    if out_path:
        encoded_image.save(out_path, quality = 100)

    return encoded_image

def encode_data_from_path(img_path: str, message: str, out_path: str = None) -> Image.Image:
    """Encodes a string within an image."""
    # open image
    image: Image.Image = Image.open(img_path)

    encoded_image: Image.Image = _encode_data(image, message)

    if out_path:
        encoded_image.save(out_path, quality = 100)

    return encoded_image

def _encode_data(image: Image.Image, message: str) -> Image.Image:
    image_size: tuple[int, int] = image.size
    num_pixels: int = image.size[0] * image.size[1]

    binary_array: list[tuple[int, int, int]] = _str_to_binary_tuples(message)

    if len(binary_array) > num_pixels // 3:
        raise ValueError("Cannot encode data: message too long")

    for pixel_index, bits in enumerate(binary_array):
        col: int = pixel_index // image_size[0]
        row: int = pixel_index % image_size[0]
        pixel_rgb_values = image.getpixel((row, col))

        new_pixel_rgb_values = []

        # alter rgb values to encode data (0 = even, 1 = odd)
        for rgb_index, rgb_value in enumerate(pixel_rgb_values):
            if rgb_value % 2 != bits[rgb_index]:
                rgb_value += 1

            new_pixel_rgb_values.append(rgb_value)

        image.putpixel((row, col), tuple(new_pixel_rgb_values))

    return image


def decode_data(image: Image.Image) -> str:
    """Decodes the string within the image."""
    return _decode_data(image)

def decode_data_from_path(img_path: str) -> str:
    """Decodes the string within the image."""
    image: Image.Image = Image.open(img_path)
    return _decode_data(image)

def _decode_data(image: Image.Image) -> str:
    """Decodes the string within the image."""
    image_data = image.getdata()

    bytes_list: list[str] = []
    current_bytes: list[str] = []
    current_byte = ""
    num_encoded_bytes = None

    for index, rgb_tuple in enumerate(image_data):
        if num_encoded_bytes is not None and index // 3 > num_encoded_bytes:
            break

        for bit in rgb_tuple:
            current_byte += str(bit % 2)

        # every complete byte
        if index % 3 == 2:
            if current_byte[0] == "0":
                # same char
                current_bytes.append(current_byte[1:])
            elif current_byte[0] == "1":
                # different char
                if num_encoded_bytes is None:
                    current_bytes = current_bytes or [current_byte[1:]]
                    num_encoded_bytes = int(r"0b" + "".join(current_bytes), 2)

                    current_bytes = []
                else:
                    if len(current_bytes) != 0:
                        bytes_list.append("".join(current_bytes))

                    current_bytes = [current_byte[1:]]

            current_byte = ""

    # add leftover bytes
    bytes_list.append("".join(current_bytes))

    char_list: list[str] = [chr(int(char_bytes, 2)) for char_bytes in bytes_list]

    message: str = "".join(char_list)

    return message