import io

import wx

from .. import utils


class WFParameter(dict):
    PFLAG_VALUE = 0
    # PFLAG_UNKNOWN = 1
    PFLAG_HAS_CHILDREN = 2
    # PFLAG_UNKNOWN2 = 4

    def __init__(self, id: int = None, val: int = None) -> None:
        d = {}
        if not(id is None or val is None):
            d[id] = val
        super().__init__(d)

    @classmethod
    def read_one(cls, buf: io.BytesIO) -> 'WFParameter':
        raw_id = utils.io2int(buf, 1)
        _id = (raw_id & 0xf8) >> 3
        flag = raw_id & 0x07

        if not _id:
            raise ValueError(f'Invalid Parameter ID {raw_id=:02x}')

        v = cls.read_val(buf)
        if flag == cls.PFLAG_HAS_CHILDREN:
            x = buf.read(v)
            v = cls.read_list(io.BytesIO(x), len(x))
        elif flag != cls.PFLAG_VALUE:
            raise ValueError(f'Unknown Flag {flag}')
        return cls(_id, v)

    @classmethod
    def read_list(cls, buf: io.BytesIO, size: int) -> 'WFParameter':
        res = cls()
        try:
            while buf.tell() < size:
                res.update(cls.read_one(buf))
        except ValueError as e:
            wx.LogWarning(str(e) + f' in {buf.tell()}')
        if not res:
            raise ValueError('Empty child')
        return res

    @staticmethod
    def read_val(buf: io.BytesIO) -> int:
        offset = v = 0
        while 1:
            curr = utils.io2int(buf, 1)
            v |= ((curr & 0x7f) << offset)
            if not (curr & 0x80):
                return v
            offset += 7
            if offset > 56:
                raise ValueError('Value of the parameter is too long')

    @classmethod
    def write_one(cls, buf: io.BytesIO, id: int, val: [int, 'WFParameter']) -> None:
        assert 0 < id < 0x20

        id = (id << 3) & 0xF8
        if isinstance(val, cls):
            buf.write(bytes([(cls.PFLAG_HAS_CHILDREN & 0x07) | id]))
            val.write_list(buf)
        elif isinstance(val, int):
            buf.write(bytes([(cls.PFLAG_VALUE & 0x07) | id]))
            cls.write_val(buf, val)
        else:
            raise TypeError(f'val: \'int\' or \'{cls.__name__}\' expected, got {type(val)} instead')

    def write_list(self, buf: io.BytesIO, store_len=True) -> int:
        tmp = io.BytesIO()
        for id, v in self.items():
            self.write_one(tmp, id, v)
        tmp = tmp.getvalue()
        if store_len:
            self.write_val(buf, len(tmp))
        buf.write(tmp)
        return len(tmp)

    @staticmethod
    def write_val(buf: io.BytesIO, val: int) -> None:
        x = []
        if not val:
            x.append(val)
        while val:
            x.append((val & 0x7f) | 0x80)
            val >>= 7
        try:
            x[-1] &= 0x7f
        except IndexError as e:
            wx.LogWarning(str(e))
            raise
        buf.write(bytes(x))
