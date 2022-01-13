import io
import os

import wx

from typing import BinaryIO

from . import elements, errors, utils
from .wfimage import WFImage
from .wfparameter import WFParameter


class WatchFace:
    WF_VER = {
        b'HMDIAL\x00': 4,
        b'UIHH\x01\x00\xFF': -1
    }
    HDR_LEN = {
        -1: 87,
        4: 40,
        5: 87,
        6: 87,
    }

    def __init__(self, version=None, hdr=None, main_param=None, elems=None, images=None, params=None):
        self.version = version
        self.hdr = hdr
        self.main_param = main_param
        self.elements = elems
        self.images = images
        self.params = params

    @classmethod
    def from_file(cls, fn):
        wx.LogMessage(f'Reading {fn}')
        fsz = os.stat(fn).st_size
        with open(fn, 'rb') as f:
            ver = cls.WF_VER.get(f.read(7))
            if ver is None:
                raise errors.WFFileFormatError()
            hdr_sz = cls.HDR_LEN.get(ver)

            f.seek(0)
            hdr = f.read(hdr_sz)
            if ver == -1:
                pass
            hdr_params_size = utils.b2i(hdr[-4:])
            hdr_params = io.BytesIO(f.read(hdr_params_size))

            main_param = elements.MainParams(WFParameter.read_one(hdr_params).get(1))
            elems = {1: main_param}
            param_loc = WFParameter.read_list(hdr_params, hdr_params_size)
            params = io.BytesIO(f.read(main_param.table_len))
            offsets = list(utils.io2int(f, 4) for _ in range(main_param.images_cnt))
            offsets.sort()
            offsets.append(fsz)

            images = cls._images_collect(f, offsets)
            # elems.update(cls._elements_collect(params, param_loc))
            p = cls._elements_collect(params, param_loc)

        return cls(ver, hdr, main_param, elems, images, p)

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
            try:
                res = WFImage.from_bytes(buf)
                # res.img.save(f'images/{i}.png')
            except Exception as e:
                wx.LogWarning(f'{e}. Save as bytes')
                res = buf
            result.append(res)
        return result

    @staticmethod
    def _elements_collect(params: io.BytesIO, params_loc: WFParameter):
        # result = {}
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
