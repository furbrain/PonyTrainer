#!/usr/bin/python3

import time
import bootloader
import hexfile
import sys
import datetime
    
def show_progress(i):
    if i==0:
        show_progress.counter = 0
        return
    if i > show_progress.counter:
        sys.stdout.write(".")
        sys.stdout.flush()
        show_progress.counter = i
                
try:
    print("Connecting to device")
    prog = bootloader.Programmer()
    print("%s found" % prog.get_name())
    fw_info = prog.get_fw_info()
    #config = prog.read_program(fw_info.config.location, fw_info.config.size)
    #legs = prog.read_program(fw_info.legs.location, fw_info.legs.size)    
    print("Loading hexfile")
    hexfile  = hexfile.HexFile(sys.argv[1])
    #print("Merging config")
    #hexfile.insert(fw_info.config.location, config)
    #print("Merging legs")
    #hexfile.insert(fw_info.legs.location, legs)

    print("Programming %d bytes" % len(hexfile))
    show_progress(0)
    prog.write_program(hexfile,set_progress=show_progress)
    print("Verifying %d bytes" % len(hexfile))
    show_progress(0)
    prog.verify_program(hexfile,set_progress=show_progress)
    print("Setting Time")
    prog.write_datetime(datetime.datetime.now())
    print("Programming complete")
except bootloader.ProgrammerError as e:
    print(e)
    sys.exit(1)
sys.exit(0)
