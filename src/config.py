#!/usr/bin/python3
from src.version import Version
from .struct_parser import StructParser


class Config(StructParser):
    FMT = [
        ('axes', [
            ('accel', '3B'),
            ('mag', '3B')
        ]),
        ('dummy', 'h'),
        ('calib', [
            ('accel', '12f'),
            ('mag', '12f'),
            ('laser_offset', 'f')
        ]),
        ('display_style', 'B'),
        ('length_units', 'B'),
        ('timeout', 'h'),
        ('bluetooth', 'B')
    ]
    ALIGNMENT = 8

    def is_valid(self):
        return self.axes.accel[0] < 3


class Config2(StructParser):
    FMT = [
        ('axes', [
            ('accel', '3B'),
            ('mag', '3B')
        ]),
        ('dummy', 'h'),
        ('calib', [
            ('accel', '21f'),
            ('mag', '21f'),
            ('laser_offset', 'f')
        ]),
        ('display_style', 'B'),
        ('length_units', 'B'),
        ('timeout', 'h'),
        ('bluetooth', 'B')
    ]
    ALIGNMENT = 8

    def is_valid(self):
        return self.axes.accel[0] < 3

config_map = {
    1: Config,
    2: Config2
}


def default_config():
    c = Config.create_empty()
    c.axes.accel = [4, 0, 5]
    c.axes.mag = [0, 4, 5]
    c.dummy = 0
    c.calib.accel = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    c.calib.mag = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    c.calib.laser_offset = 0.090
    c.display_style = 0
    c.length_units = 0
    c.timeout = 120
    return c


def get_config(programmer):
    fw_info = Version.from_data_source(programmer)
    config_class = config_map[fw_info.config.version]
    conf = default_config()
    for i in range(fw_info.config.location, fw_info.config.location + fw_info.config.size, config_class.get_len()):
        text = programmer.read_program(i, config_class.get_len())
        if text[0] == 0xff:
            break
        conf = config_class.from_buffer(text)
    return conf


if __name__ == "__main__":
    from . import bootloader

    loader = bootloader.Programmer()
    print(get_config(loader))
