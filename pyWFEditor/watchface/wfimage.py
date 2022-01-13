import struct


class WFImage:
    SIGNATURE = b'BM'
    FMT = '<2s7H'
    HDR_SZ = struct.calcsize(FMT)
    _16IF = '<H'
    _16IF_SZ = struct.calcsize(_16IF)
    _24IF = '>BH'
    _24IF_SZ = struct.calcsize(_24IF)

    def __init__(self, width, height, row_len, bpp, palette_cols, is_transp, unknown, buf: bytes):
        if palette_cols > 256:
            raise ValueError('Too many palette colors')
        if not (palette_cols or bpp in (8, 16, 24, 32)):
            raise ValueError(f'Unsupported bits per pixel value: {bpp}')
        self.row_len = row_len
        self.bpp = bpp
        self.palette_cols = palette_cols
        self.is_transp = is_transp
        self.unknown = unknown
        self.img = None

    @classmethod
    def from_file(cls, fname):
        raise NotImplementedError()

    @classmethod
    def from_bytes(cls, buf: bytes):
        sign, unknown, width, height, row_len, bpp, palette_cols, is_transp = struct.unpack_from(cls.FMT, buf)

        if sign != cls.SIGNATURE:
            raise ValueError(f'Invalid signature {sign}')

        return cls(width, height, row_len, bpp, palette_cols, is_transp, unknown, buf[cls.HDR_SZ:])
