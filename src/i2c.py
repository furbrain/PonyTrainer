#!/usr/bin/python3

import sys

from . import bootloader

try:
    print("Connecting to device")
    programmer = bootloader.Programmer()
    print("Device found, resetting")
    print(programmer.read_i2c(0x3c, 1))
except bootloader.ProgrammerError as e:
    print(e)
    sys.exit(1)
sys.exit(0)
