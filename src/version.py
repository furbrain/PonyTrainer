#!/usr/bin/env python3
import sys
from functools import total_ordering

from .struct_parser import StructParser

SOFTWARE_VERSION="0.0.1"
FIRMWARE_INFO_LOCATION = 0x9D008100

@total_ordering
class Version(StructParser):

    FMT = [
        ('version', [
            ('major', 'B'),
            ('minor',   'B'),
            ('revision', 'B'),
            ('checksum','B')
            ]),
        ('config', [
            ('location', 'I'),
            ('size', 'H'),
            ('version', 'B'), 
            ('dummy','B')
            ]),
        ('legs', [
            ('location', 'I'),
            ('size', 'H'),
            ('version', 'B'), 
            ('dummy','B')
            ]),
        ('calibration', [
            ('location', 'I'),
            ('size', 'H'),
            ('version', 'B'), 
            ('dummy','B')
            ]),
    ]



    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def __lt__(self, other):
        return self.as_tuple() < other.as_tuple()

    def is_valid(self):
        v = self.version
        checksum = v.major ^ v.minor ^ v.revision ^ 0x55
        return checksum == v.checksum

    @staticmethod
    def from_data_source(source) -> "Version":
        data = source.get_data_slice(FIRMWARE_INFO_LOCATION, Version.get_len())
        return Version.from_buffer(data)

    def as_semantic(self):
        return f"v{self.version.major}.{self.version.minor}.{self.version.revision}"

    def as_tuple(self):
        return (self.version.major, self.version.minor, self.version.revision)

if __name__ == "__main__":
    from . import bootloader
    from . import hexfile

    try:
        print("Connecting to device")
        prog = bootloader.Programmer()
        print("Device found, reading data")
        version = Version.from_data_source(prog)
        print(version)
        print(version.is_valid())
    except bootloader.ProgrammerError as e:
        print(e)
    if len(sys.argv)>1:
        print("Reading file: ", sys.argv[1])
        hex = hexfile.HexFile(sys.argv[1])
        version = Version.from_data_source(hex)
        print(version)
        print(version.is_valid())

