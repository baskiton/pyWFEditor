import hashlib
import io
import os
import struct

from typing import Optional

import wx

from .. import utils


class WFImage:
    _SIGNATURE = b'BM'
    _FMT = '<2s7H'
    _HDR_SZ = struct.calcsize(_FMT)
    _PLT_FMT = '>4B'
    _PLT_FMT_SZ = struct.calcsize(_PLT_FMT)

    def __init__(self, path: str = None, name: str = None) -> None:
        assert path or name
        self.path = path
        self.name = name or os.path.basename(path)
        x = hashlib.blake2b((self.name + (self.path or '')).encode(), digest_size=8)
        self.id, = struct.unpack('<q', x.digest())
        self.img: Optional[wx.Image] = None

    def get_image(self) -> wx.Image:
        if self.img:
            return self.img
        elif self.path:
            return wx.Image(self.path)

    def gen_image(self, buf: bytes = None) -> wx.Image:
        if buf:
            self.from_bytes(buf)
        elif self.path:
            self.img = wx.Image(self.path)
        else:
            raise ValueError('No data for generate image')
        return self.img

    def from_bytes(self, buf: bytes) -> None:
        sign, unknown, width, height, row_len, bpp, palette_cols, is_transp = struct.unpack_from(self._FMT, buf)
        off = self._HDR_SZ

        if sign != self._SIGNATURE:
            raise ValueError(f'Invalid signature {sign}')
        if palette_cols > 256:
            raise ValueError('Too many palette colors')
        if not (palette_cols or bpp in (8, 16, 24, 32)):
            raise ValueError(f'Unsupported bits per pixel value: {bpp}')

        if palette_cols:
            off, palette = self._get_palette(buf, off, palette_cols, is_transp)
            div, divider = (bpp / 8).as_integer_ratio()
            mask = 2 ** bpp - 1
            ad = divider - 1

            def get_rgba(_buf: io.BytesIO):
                nonlocal ad
                base = _buf.tell()
                idx = utils.io2int(_buf, div)
                idx = (idx >> (bpp * ad)) & mask
                ad -= 1
                if ad < 0:
                    ad += divider
                else:
                    _buf.seek(base)
                return palette[idx]

        elif bpp == 8:
            def get_rgba(_buf: io.BytesIO):
                c = utils.io2int(_buf, 1)
                return c, c, c, 0xFF

        elif bpp == 16:
            def get_rgba(_buf: io.BytesIO):
                rgb565 = utils.io2int(_buf, 2, 'little')
                return *utils.rgb565_to_rgb(rgb565), 0xFF

        elif bpp == 24:
            def get_rgba(_buf: io.BytesIO):
                a = utils.io2int(_buf, 1)
                rgb565 = utils.io2int(_buf, 2, 'big')
                return *utils.rgb565_to_rgb(rgb565), 0xFF - a

        elif bpp == 32:
            def get_rgba(_buf: io.BytesIO):
                r = utils.io2int(_buf, 1)
                g = utils.io2int(_buf, 1)
                b = utils.io2int(_buf, 1)
                a = utils.io2int(_buf, 1)
                return r, g, b, 0xFF - a

        else:   # unreach
            raise ValueError(f'Unsupported bits per pixel value: {bpp}')

        self.img = wx.Image(width, height)
        self.img.InitAlpha()
        for y in range(height):
            off_n = off + row_len
            row = io.BytesIO(buf[off:off_n])
            off = off_n
            if palette_cols:
                ad = divider - 1
            for x in range(width):
                r, g, b, a = get_rgba(row)
                self.img.SetRGB(x, y, r, g, b)
                self.img.SetAlpha(x, y, a)

    def _get_palette(self, buf: bytes, off: int, palette_cols: int, is_transp: bool) -> tuple[int, list]:
        palette = []    # idx: (r, g, b, a)
        for i in range(palette_cols):
            r, g, b, _ = struct.unpack_from(self._PLT_FMT, buf, off)
            off += self._PLT_FMT_SZ
            if _:
                wx.LogWarning(f'Palette item {i}: padding is not zero: {_:02X}')
            a = 0x00 if (is_transp and not i) else 0xFF
            palette.append((r, g, b, a))

        return off, palette
