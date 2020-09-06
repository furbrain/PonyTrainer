#!/usr/bin/python3

import struct
import sys

from . import bootloader

address = int(sys.argv[1], 0)
size = int(sys.argv[2], 0)

try:
    print("Connecting to device")
    programmer = bootloader.Programmer()
    print("Device found, reading data")
    data = programmer.read_program(address, size)
    i = 0
    print(len(data))
    while i < len(data):
        x, = struct.unpack_from("I", data, i)
        i += 4
        print("0x{:08x}\n".format(x))
except bootloader.ProgrammerError as e:
    print(e)
    sys.exit(1)
sys.exit(0)
