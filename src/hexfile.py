#!/usr/bin/env python3 
import operator
from functools import reduce

import sparse_list

from . import version


class HexFileError(Exception):
    def _init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class HexFile:
    def __init__(self, fname):
        self.program = sparse_list.SparseList(0x100000000)
        page = 0
        with open(fname, "r") as f:
            for s in f:
                if s[0] == ":":
                    # good - it starts sensibly...
                    numbers = bytearray.fromhex(s.strip()[1:])
                    record_length = numbers[0]
                    offset = numbers[1] * 256 + numbers[2]
                    rectype = numbers[3]
                    data = numbers[4:-1]
                    checksum = reduce(operator.add, numbers) & 0xff
                    if (checksum != 0) or (record_length != len(data)):
                        raise HexFileError("Bad checksum")
                else:
                    raise HexFileError("Bad format")
                # so far, so good. Now to slot the data in...
                if rectype not in (0, 1, 4):
                    # rectype not known. Fall over
                    raise HexFileError("Unknown record format")
                if rectype == 0:
                    self.program[page + offset:page + offset + record_length] = data
                if rectype == 1:
                    # end of file
                    return
                if rectype == 4:
                    if offset != 0:
                        # really should be zero...
                        raise HexFileError("Bad format")
                    if record_length != 2:
                        # incorrect length
                        raise HexFileError("Bad format")
                    page = data[0] * 0x1000000 + data[1] * 0x10000
                    page = page | 0x80000000

    def __len__(self):
        return len(self.program.elements)

    def insert(self, address, data):
        length = len(data)
        self.program[address:address + length] = data

    def get_data_slice(self, address, length):
        data = self.program[address: address + length]
        data = [0 if x is None else x for x in data]
        return bytes(data)


if __name__ == "__main__":
    import sys

    hexfile = HexFile(sys.argv[1])
    info = version.Version.from_data_source(hexfile)
    print(info)
