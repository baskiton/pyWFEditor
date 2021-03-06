import io
import pprint

from typing import BinaryIO

import wx

from . import elements, errors
from .. import utils
from ..utils import quicklz
from .wfimage import WFImage
from .wfparameter import WFParameter


class WFHeader:
    H_SIGN = b'HMDIAL\x00'
    U_SIGN = b'UIHH'
    SIGN_LEN = {
        b'H': len(H_SIGN),
        b'U': len(U_SIGN),
    }
    VER_POS = {
        H_SIGN: 0x0B,
        U_SIGN: 0x04,
    }

    H_HDR_LEN = {
        0xFF: 40,
        0x06: 64,
    }
    H_DEV_ID_LOC = 0x10

    U_VER_NORMAL = 0x01
    U_VER_COMPRESS = 0x02
    U_COMPRESS_START = 0x28
    U_HDR_LEN = 87

    def __init__(self, buf: BinaryIO):
        self.unknown0 = self.unknown1 = self.hdr_params_size = self.device_id = self.version = -1

        buf.seek(0)
        if utils.io2int(buf, 1) == 0x4F:   # qlz packed
            unc = quicklz.qlz_stream_decompress(buf)
            buf.seek(0)
            buf.write(unc)
            wx.LogDebug('file compressed. Decompress OK')

        buf.seek(0)
        s_len = self.SIGN_LEN.get(buf.read(1))
        if s_len is None:
            raise errors.WFFileFormatError()

        buf.seek(0)
        sign = buf.read(s_len)
        if sign == self.H_SIGN:
            self.hmdial_build(buf)
        elif sign == self.U_SIGN:
            self.uihh_build(buf)
        else:
            raise errors.WFFileFormatError()

    def hmdial_build(self, buf):
        buf.seek(self.VER_POS[self.H_SIGN])
        self.version = utils.io2int(buf, 1)
        hdr_len = self.H_HDR_LEN.get(self.version)
        if not hdr_len:
            raise errors.WFFileFormatError()
        buf.seek(self.H_DEV_ID_LOC)
        self.device_id = utils.io2int(buf, 1)
        buf.seek(hdr_len - 12)
        self.unknown1 = utils.io2int(buf, 4, signed=True)
        self.hdr_params_size = utils.io2int(buf, 4, signed=True)
        self.unknown0 = utils.io2int(buf, 4, signed=True)

    def uihh_build(self, buf):
        buf.seek(self.VER_POS[self.U_SIGN])
        self.version = utils.io2int(buf, 2)
        if self.version == self.U_VER_COMPRESS:
            buf.seek(0)
            buf.seek(self.U_COMPRESS_START)
            unc = quicklz.qlz_stream_decompress(io.BytesIO(buf.read()))
            buf.seek(self.U_COMPRESS_START)
            buf.write(unc)

        # TODO: find device id
        buf.seek(self.U_HDR_LEN - 12)
        if self.version == self.U_VER_NORMAL:
            v = 'unknown1', 'unknown0', 'hdr_params_size'
        else:   # U_VER_COMPRESS
            v = 'unknown1', 'hdr_params_size', 'unknown0'
            buf.seek(1, io.SEEK_CUR)
        for i in v:
            setattr(self, i, utils.io2int(buf, 4, signed=True))


class WatchFace:
    def __init__(self, hdr=None, main_param=None, elems=None, images=None, params=None):
        self.hdr = hdr
        self.main_param = main_param
        self.elements = elems
        self.images = images
        self.params = params

    @classmethod
    def from_file(cls, fn):
        wx.LogMessage(f'Reading {fn}')

        f = io.BytesIO(open(fn, 'rb').read())

        hdr = WFHeader(f)
        hdr_params = io.BytesIO(f.read(hdr.hdr_params_size))

        main_param = elements.MainParams(WFParameter.read_one(hdr_params).get(1))
        wx.LogDebug(str(main_param))
        wx.LogDebug(f'hdr_params_size={hdr.hdr_params_size}')
        elems = {1: main_param}

        param_loc = WFParameter.read_list(hdr_params, hdr.hdr_params_size)
        hdr_params.close()
        params = io.BytesIO(f.read(main_param.table_len))

        cur = f.tell()
        f.seek(0, io.SEEK_END)
        fsz = f.tell()
        f.seek(cur)

        offsets = []
        for _ in range(main_param.images_cnt):
            v = utils.io2int(f, 4, signed=True)
            if v > fsz or v < 0:
                f.seek(-4, io.SEEK_CUR)
                break
            offsets.append(v)
        # offsets = list(utils.io2int(f, 4) for _ in range(main_param.images_cnt))
        # offsets.sort()
        offsets.append(fsz)

        _s = io.StringIO()
        pprint.pprint(param_loc, width=3, stream=_s)
        wx.LogDebug('\n' + _s.getvalue())
        # wx.LogDebug(offsets, width=3)

        images = p = None
        # images = cls._images_collect(f, offsets)
        # elems.update(cls._elements_collect(params, param_loc))
        p = cls._elements_collect(params, param_loc)

        return cls(hdr, main_param, elems, images, p)

    @staticmethod
    def _images_collect(f: BinaryIO, offsets: list):
        res_start = f.tell()
        result = []
        for i, off in enumerate(offsets[:-1]):
            f.seek(res_start + off)
            buf = f.read(offsets[i + 1] - off)
            sign = buf[:2]
            if sign != b'BM':
                raise errors.WFImageFormatError(sign)
            img = WFImage(name=f'{i:03}')
            try:
                res = img.gen_image(buf)
                # res.SaveFile(f'0images/{img.name}.png')
            except Exception as e:
                wx.LogWarning(f'Error in "{img.name}": {e}. Binary dumped. Store as bytes')
                with open(f'0dumped/{img.name}.bin', 'wb') as fi:
                    fi.write(buf)
                res = buf
            result.append(res)
        return result

    @staticmethod
    def _elements_collect(params: io.BytesIO, params_loc: WFParameter):
        result = WFParameter()
        for pid, loc in params_loc.items():
            loff = loc[1]
            llen = loc[2]
            params.seek(loff)
            param = WFParameter.read_list(io.BytesIO(params.read(llen)), llen)
            result[pid] = param

            # if pid == 2:
            #     e = elements.Background(param)
            # elif pid == 3:
            #     e = elements.Time(param)
            # elif pid == 4:
            #     e = elements.Activity(param)
            # elif pid == 5:
            #     e = elements.Date(param)
            # elif pid == 6:
            #     e = elements.Weather(param)
            # elif pid == 7:
            #     e = elements.StepsProgress(param)
            # elif pid == 8:
            #     e = elements.Status(param)
            # elif pid == 9:
            #     e = elements.Battery(param)
            # # elif pid == 10:
            # #     e = elements.AnalogDialFace(param)
            # elif pid == 11:
            #     e = elements.Blink(param)
            # else:
            #     wx.LogWarning(f'Unknown element id {pid}')
            #     continue
            # result[pid] = e
        return result
