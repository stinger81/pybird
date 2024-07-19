# /bin/python3
# ##########################################################################
#
#   Copyright (C) 2022-2024 Michael Dompke (https://github.com/stinger81)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Michael Dompke (https://github.com/stinger81)
#   michael@dompke.dev
#
# ##########################################################################

import struct


####################################################################################################
# region Bytes
def write_bytes(in_bytes: bytes) -> bytes:
    if in_bytes is None or len(in_bytes) == 0:
        my_bytes: bytes = write_uint8(0)
    else:
        my_bytes: bytes = write_uint8(len(in_bytes))
        my_bytes += in_bytes
    return my_bytes


def read_bytes(in_bytes: bytes, in_index: int = 0) -> tuple[bytes, int]:
    my_bytes: bytes = bytes()
    (my_len, my_index) = read_uint8(in_bytes, in_index)
    if my_len > 0:
        my_bytes = in_bytes[my_index: my_index + my_len]
        my_index += my_len
    return my_bytes, my_index


def write_bytes_len(in_bytes: bytes) -> bytes:
    return in_bytes


def read_bytes_len(in_bytes: bytes, in_index: int = 0, in_length: int = 1) -> tuple[bytes, int]:
    if in_length > 0:
        return in_bytes[in_index:in_index + in_length], in_index + in_length
    else:
        return b'', in_index


# endregion
####################################################################################################
####################################################################################################
# region bool
def write_bool(in_bool: bool) -> bytes:
    if in_bool:
        return write_int8(1)
    else:
        return write_int8(0)


def read_bool(in_bytes: bytes, in_index: int = 0) -> tuple[bool, int]:
    (my_bool, my_offset) = read_int8(in_bytes, in_index)
    if my_bool == 0:
        return False, my_offset
    else:
        return True, my_offset


# endregion
####################################################################################################
####################################################################################################
# region Text
def write_text(in_str: str) -> bytes:
    return write_bytes(in_str.encode('utf-8'))


def read_text(in_bytes: bytes, in_index: int = 0) -> tuple[str, int]:
    (my_byte, my_index) = read_bytes(in_bytes, in_index)
    return my_byte.decode('utf-8'), my_index


# end Region
####################################################################################################
####################################################################################################
# region Integers
def write_int8(in_int: int) -> bytes:
    return struct.pack('!b', in_int)


def read_int8(in_bytes: bytes, in_index: int = 0) -> tuple[int, int]:
    return struct.unpack_from('!b', in_bytes[in_index: in_index + 1])[0], in_index + 1


def write_uint8(in_int: int) -> bytes:
    return struct.pack('!B', in_int)


def read_uint8(in_bytes: bytes, in_index: int = 0) -> tuple[int, int]:
    return struct.unpack_from('!B', in_bytes[in_index: in_index + 1])[0], in_index + 1


def write_int16(in_int: int) -> bytes:
    return struct.pack('!h', in_int)


def read_int16(in_bytes: bytes, in_index: int = 0) -> tuple[int, int]:
    return struct.unpack_from('!h', in_bytes[in_index: in_index + 2])[0], in_index + 2


def write_uint16(in_int: int) -> bytes:
    return struct.pack('!H', in_int)


def read_uint16(in_bytes: bytes, in_index: int = 0) -> tuple[int, int]:
    return struct.unpack_from('!H', in_bytes[in_index: in_index + 2])[0], in_index + 2


def write_int32(in_int: int) -> bytes:
    return struct.pack('!i', in_int)


def read_int32(in_bytes: bytes, in_index: int = 0) -> tuple[int, int]:
    return struct.unpack_from('!i', in_bytes[in_index: in_index + 4])[0], in_index + 4


def write_uint32(in_int: int) -> bytes:
    return struct.pack('!I', in_int)


def read_uint32(in_bytes: bytes, in_index: int = 0) -> tuple[int, int]:
    return struct.unpack_from('!I', in_bytes[in_index: in_index + 4])[0], in_index + 4


def write_int64(in_int: int) -> bytes:
    return struct.pack('!q', in_int)


def read_int64(in_bytes: bytes, in_index: int = 0) -> tuple[int, int]:
    return struct.unpack_from('!q', in_bytes[in_index: in_index + 8])[0], in_index + 8


def write_uint64(in_int: int) -> bytes:
    return struct.pack('!Q', in_int)


def read_uint64(in_bytes: bytes, in_index: int = 0) -> tuple[int, int]:
    return struct.unpack_from('!Q', in_bytes[in_index: in_index + 8])[0], in_index + 8


# endregion
####################################################################################################
####################################################################################################
# region Float

def write_float(in_int: float) -> bytes:
    return struct.pack('!f', in_int)


def read_float(in_bytes: bytes, in_index: int = 0) -> tuple[float, int]:
    return struct.unpack_from('!f', in_bytes[in_index: in_index + 4])[0], in_index + 4


def write_double(in_int: float) -> bytes:
    return struct.pack('!d', in_int)


def read_double(in_bytes: bytes, in_index: int = 0) -> tuple[float, int]:
    return struct.unpack_from('!d', in_bytes[in_index: in_index + 8])[0], in_index + 8

# endregion
####################################################################################################
