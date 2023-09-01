from PIL import Image


def add_message_to_image(image: Image.Image, message: bytes) -> None:
    """Hide a message in an image by changing the least significant bit of each pixel.

    For ease of decoding, the message is prefixed with its length as a 64-bit
    big-endian integer. Each byte of the message is then spread across the
    least significant bit of eight consecutive pixels.
    """
    length = len(message)
    data = bytearray(image.tobytes())
    if length > 2**64 or (length + 8) * 8 > len(data):
        msg = "Message is too long to fit in image."
        raise ValueError(msg)
    message = length.to_bytes(8, "big") + message
    for byte_idx, message_byte in enumerate(message):
        base_bit_idx = byte_idx * 8
        for bit_offset in range(8):
            bit_idx = base_bit_idx + bit_offset
            pixel = data[bit_idx] & 0b1111_1110
            flag = (message_byte >> bit_offset) & 1
            data[bit_idx] = pixel | flag
    image.frombytes(data)


def decode_message_from_image(image: Image.Image) -> bytes:
    """Extract a message from an image by reading the least significant bit of each pixel."""
    data = bytes(image.tobytes())
    raw_length = _read_bytes_from_image(data, 0, 8)
    length = int.from_bytes(raw_length, "big")
    return _read_bytes_from_image(data, 64, length)


def _read_bytes_from_image(image_data: bytes, offset: int, length: int) -> bytes:
    """Read a number of bytes from an image, starting at a given offset.

    :param image_bytes: The raw bytes of the image to read from.
    :param offset: The number of pixels to skip before reading.
    :param length: The number of bytes to read.
    :return: The bytes read from the image.
    :raises ValueError: If the message data would exceed the size of the image.
    """
    if (offset + length * 8) > len(image_data):
        msg = "Image does not contain a message."
        raise ValueError(msg)
    message = bytearray()
    for bit_idx in range(offset, offset + length * 8):
        local_bit_idx = bit_idx & 0b111
        if local_bit_idx == 0:
            message.append(0)
        message[-1] |= (image_data[bit_idx] & 1) << local_bit_idx
    return bytes(message)
