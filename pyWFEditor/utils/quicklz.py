# Python implemented of Fast Data Compression library (quicklz)
# Currently implemented decompression with compression level 3
# (default value for resource packer/unpacker).

__all__ = (
    'qlz_decompress',
    'qlz_stream_decompress',
)

import io

from typing import BinaryIO


# QLZ_COMPRESSION_LEVEL = 3
# if QLZ_COMPRESSION_LEVEL == 3:
#     QLZ_POINTERS = 16
#     QLZ_HASH_VALUES = 4096

MINOFFSET = 2
UNCONDITIONAL_MATCHLEN = 6
UNCOMPRESSED_END = 4
CWORD_LEN = 4


def _b2i(buf: bytes, order='little', signed=False):
    return int.from_bytes(buf, order, signed=signed)


def _io2int(b: [io.BytesIO, BinaryIO], sz, order='little', signed=False):
    v = b.read(sz)
    if not v:
        raise EOFError
    return _b2i(v, order, signed)


def _qlz_fast_read(buf: bytes, start: int, size: int) -> int:
    return _b2i(buf[start:start + size])


def _qlz_get_n(i: int) -> int:
    return 4 if ((i & 2) == 2) else 1


def _qlz_size_decompressed(buf: bytes) -> int:
    n = _qlz_get_n(buf[0])
    r = _qlz_fast_read(buf, n + 1, n) if (1 <= n <= 4) else 0
    return r & (0xffffffff >> ((4 - n) * 8))


def _qlz_size_compressed(buf: bytes) -> int:
    n = _qlz_get_n(buf[0])
    r = _qlz_fast_read(buf, 1, n) if (1 <= n <= 4) else 0
    return r & (0xffffffff >> ((4 - n) * 8))


def _qlz_size_header(buf: bytes) -> int:
    return 2 * _qlz_get_n(buf[0]) + 1


def _qlz_decompress_core(buf: bytes, d_sz: int) -> bytearray:
    result = bytearray(d_sz)
    src = _qlz_size_header(buf)
    dst = 0
    last_destination_byte = d_sz - 1
    cword_val = 1
    last_matchstart = last_destination_byte - UNCONDITIONAL_MATCHLEN - UNCOMPRESSED_END
    last_source_byte = _qlz_size_compressed(buf) - 1
    bitlut = [4, 0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0]

    while 1:
        if cword_val == 1:
            # memory safe
            if src + CWORD_LEN - 1 > last_source_byte:
                return bytearray()

            cword_val = _qlz_fast_read(buf, src, CWORD_LEN)
            src += CWORD_LEN

            # memory safe
            if src + 4 - 1 > last_source_byte:
                return bytearray()

        fetch = _qlz_fast_read(buf, src, 4)

        if (cword_val & 1) == 1:
            # if QLZ_COMPRESSION_LEVEL == 3:
            cword_val >>= 1
            if not (fetch & 3):
                offset = (fetch & 0xFF) >> 2
                matchlen = 3
                src += 1
            elif not (fetch & 2):
                offset = (fetch & 0xFFFF) >> 2
                matchlen = 3
                src += 2
            elif not (fetch & 1):
                offset = (fetch & 0xFFFF) >> 6
                matchlen = ((fetch >> 2) & 15) + 3
                src += 2
            elif (fetch & 127) != 3:
                offset = (fetch >> 7) & 0x1FFFF
                matchlen = ((fetch >> 2) & 0x1F) + 2
                src += 3
            else:
                offset = (fetch >> 15)
                matchlen = ((fetch >> 7) & 255) + 3
                src += 4

            offset2 = dst - offset

            # memory safe
            if (offset2 < 0) or (offset2 > dst - MINOFFSET - 1):
                return bytearray()
            if matchlen > (last_destination_byte - dst - UNCOMPRESSED_END + 1):
                return bytearray()

            for i in range(matchlen):
                result[dst + i] = result[offset2 + i]
            dst += matchlen
        else:
            if dst < last_matchstart:
                n = bitlut[cword_val & 0x0F]
                result[dst:dst + 4] = buf[src:src + 4]
                cword_val >>= n
                dst += n
                src += n
            else:
                while dst <= last_destination_byte:
                    if cword_val == 1:
                        src += CWORD_LEN
                        cword_val = 1 << 31

                    # memory safe
                    if src >= (last_source_byte + 1):
                        return bytearray()

                    result[dst] = buf[src]
                    src += 1
                    dst += 1
                    cword_val >>= 1
                return result


def qlz_decompress(buf: bytes) -> bytearray:
    d_sz = _qlz_size_decompressed(buf)
    if (buf[0] & 1) == 1:
        return _qlz_decompress_core(buf, d_sz)
    else:
        hdr_sz = _qlz_size_header(buf)
        return bytearray(buf[hdr_sz:hdr_sz + d_sz])


def qlz_stream_decompress(z: [io.BytesIO, BinaryIO]) -> bytes:
    z.seek(0, io.SEEK_END)
    z_size = z.tell()
    z.seek(0, io.SEEK_SET)

    compress_size = 0
    decompress_size = 0
    decompressed = bytearray()

    while 1:
        if z_size <= compress_size:
            break
        if z_size < compress_size + 9:
            break
        state = z.tell()
        flag = _io2int(z, 1) # must be 0x4F ?
        compressed_len = _io2int(z, 2)
        z.read(2)
        decompressed_len = _io2int(z, 2)
        z.read(2)
        z.seek(state)
        data = z.read(compressed_len)

        if decompressed_len == 4096:
            decompressed.extend(qlz_decompress(data))
            compress_size += compressed_len
            decompress_size += 4096
        else:
            decompressed.extend(data[:z_size - compress_size])
            decompress_size += z_size - compress_size
            compress_size = z_size
    return bytes(decompressed)
