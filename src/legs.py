#!/usr/bin/python3
import datetime

from .struct_parser import StructParser
from . import version

def get_surveys(leg_list):
    surveys = {}
    survey_nums  = {x.survey for x in leg_list}
    for s in survey_nums:
        surveys[s] = {'legs': [x for x in leg_list if x.survey==s]}   
    for s, dct in surveys.items():
        dct['survey'] = s
        dct['time'] = datetime.datetime.fromtimestamp(min(x.time for x in dct['legs']))
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

def read_legs(bootloader):
    fw_info = version.get_firmware_info(bootloader)
    data = bootloader.read_program(fw_info.legs.location, fw_info.legs.size)
    legs = Leg.read_array(data)
    return legs

def get_all_surveys(bootloader):        
    legs = read_legs(bootloader)
    surveys = get_surveys(legs)
    return surveys
    
if __name__=="__main__":
    import bootloader
    b = bootloader.Programmer()
    print(read_legs(b))