#!/usr/bin/python3

import datetime
import struct
import sys
import time

from . import bootloader

try:
    print("Connecting to device")
    programmer = bootloader.Programmer()
    print("Reading time")
    print(programmer.read_datetime())
    print("Setting Time")
    programmer.write_datetime(datetime.datetime.now())
    print("Device found, reading data")
    data = programmer.read_program(0xBF800040, 4)
    x, = struct.unpack_from("I", data)
    print("0x{:08x}\n".format(x))
    print(data)
    time.sleep(60)
    data = programmer.read_program(0xBF800040, 4)
    x, = struct.unpack_from("I", data)
    print("0x{:08x}\n".format(x))
    print(data)
except bootloader.ProgrammerError as e:
    print(e)
    sys.exit(1)
sys.exit(0)
