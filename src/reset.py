#!/usr/bin/python3

import sys

from . import bootloader

try:
    print("Connecting to device")
    programmer = bootloader.Programmer()
    print("Device found, resetting")
    programmer.reset()
except bootloader.ProgrammerError as e:
    print(e)
    sys.exit(1)
sys.exit(0)
