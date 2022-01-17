import io
from typing import BinaryIO

from .logging import Logging


__all__ = (
    'Logging',
    'WC_IMAGES',
    'b2i',
    'io2int',
    'rgb565_to_rgb',
    'quicklz',
)

_x = (
    # display, filter
    ('BMP (*.bmp)', '*.bmp'),
    ('GIF (*.gif)', '*.gif'),
    ('PNG (*.png)', '*.png'),
    ('JPEG (*.jpg)', '*.jpg'),
    ('ICO (*.ico)', '*.ico'),
    ('PNM (*.pnm)', '*.pnm'),
    ('PCX (*.pcx)', '*.pcx'),
    ('TIFF (*.tif)', '*.tif'),
    ('All Files', '*.*'),
)
WC_IMAGES = f'All supported formats|{";".join(i[1] for i in _x[:-1])}|{"|".join("|".join(i) for i in _x)}'


def b2i(buf: bytes, order='little', signed=False):
    return int.from_bytes(buf, order, signed=signed)


def io2int(b: [io.BytesIO, BinaryIO], sz, order='little', signed=False):
    v = b.read(sz)
    if not v:
        raise EOFError
    return b2i(v, order, signed)


def rgb565_to_rgb(rgb565):
    b = (rgb565 & 0b1111100000000000) >> 8
    g = (rgb565 & 0b0000011111100000) >> 3
    r = (rgb565 & 0b0000000000011111) << 3
    return r, g, b
