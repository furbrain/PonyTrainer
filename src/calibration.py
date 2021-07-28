#!/usr/bin/python3
import math

from .struct_parser import StructParser
from .version import Version


class Calibration(StructParser):
    FMT = [
        ('mag', '256f'),
        ('grav', '256f'),
    ]
    ALIGNMENT = 8

    def is_valid(self):
        return not math.isnan(self.mag[0])


CAL_CLASSES = {
    1: Calibration,
}


def read_cal(bootloader):
    fw_info = Version.from_data_source(bootloader)
    cal_class = CAL_CLASSES[fw_info.calibration.version]
    data = bootloader.read_program(fw_info.calibration.location, cal_class.get_len())
    cal = cal_class.from_buffer(data)
    return cal
