import io
from typing import BinaryIO


def b2i(buf: bytes, signed=False):
    return int.from_bytes(buf, 'little', signed=signed)


def io2int(b: [io.BytesIO, BinaryIO], sz, signed=False):
    v = b.read(sz)
    if not v:
        raise EOFError
    return b2i(v, signed)


def rgb565_to_rgb(rgb565):
    b = (rgb565 & 0b1111100000000000) >> 8
    g = (rgb565 & 0b0000011111100000) >> 3
    r = (rgb565 & 0b0000000000011111) << 3
    return r, g, b
