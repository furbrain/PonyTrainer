#!/usr/bin/python3
import datetime
import math

from .version import Version
from .struct_parser import StructParser

    
class Calibration(StructParser):
    FMT = [
        ('mag', '256f'),
        ('grav', '256f'),
    ]
    ALIGNMENT = 8
    
    def is_valid(self):
        return not math.isnan(self.mag[0])

def read_cal(bootloader):
    fw_info = Version.from_data_source(bootloader)
    data = bootloader.read_program(fw_info.calibration.location, Calibration.get_len())
    cal = Calibration.from_buffer(data)
    return cal
