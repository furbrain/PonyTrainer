#!/usr/bin/env python3
from .struct_parser import StructParser

SOFTWARE_VERSION="v1.3.0"
FIRMWARE_INFO_LOCATION = 0x9D008100
class Version(StructParser):

    FMT = [
        ('version', [
            ('major', 'B'),
            ('minor',   'B'),
            ('revision', 'B'),
            ('dummy','B')
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

def get_firmware_info(bootloader):
    data = bootloader.read_program(FIRMWARE_INFO_LOCATION, Version.get_len())
    version = Version.from_buffer(data)
    return version
    
if __name__ == "__main__":
    import bootloader

    try:
        print("Connecting to device")
        prog = bootloader.Programmer()
        print("Device found, reading data")
        print(get_firmware_info(prog))
    except bootloader.ProgrammerError as e:
        print(e)

