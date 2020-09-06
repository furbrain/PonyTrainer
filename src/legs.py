#!/usr/bin/python3
import datetime
from typing import Dict, Any

from src.version import Version
from .struct_parser import StructParser


def get_surveys(leg_list):
    surveys: Dict[int, Dict[str, Any]] = {}
    survey_nums = {x.survey for x in leg_list}
    for s in survey_nums:
        surveys[s]: Dict[str, Any] = {'legs': [x for x in leg_list if x.survey == s]}
    for s, dct in surveys.items():
        dct['survey'] = s
        dct['time'] = datetime.datetime.fromtimestamp(min([x.time for x in dct['legs']]))
        all_stations = {x.frm for x in dct['legs']}
        all_stations.update(x.to for x in dct['legs'])
        dct['station_count'] = len(all_stations)
        dct['leg_count'] = len(dct['legs'])
    return surveys


class Leg(StructParser):
    FMT = [
        ('time', 'I'),
        ('survey', 'H'),
        ('frm', 'B'),
        ('to', 'B'),
        ('delta', '3f')
    ]
    ALIGNMENT = 8

    def is_valid(self):
        return self.time != 0xffffffff


def read_legs(programmer):
    fw_info = Version.from_data_source(programmer)
    data = programmer.read_program(fw_info.legs.location, fw_info.legs.size)
    legs = Leg.read_array(data)
    return legs


def get_all_surveys(programmer):
    legs = read_legs(programmer)
    surveys = get_surveys(legs)
    return surveys


if __name__ == "__main__":
    from . import bootloader

    b = bootloader.Programmer()
    print(read_legs(b))
