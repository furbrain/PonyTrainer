#!/usr/bin/python3

import time
import bootloader
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
    config = prog.read_program(bootloader.APP_CONFIG_LOCATION, bootloader.APP_CONFIG_SIZE)
    legs = prog.read_program(bootloader.APP_LEG_LOCATION, bootloader.APP_LEG_SIZE)    
    print("Loading hexfile")
    hexfile  = bootloader.HexFile(sys.argv[1])
    print("Programming %d bytes" % len(hexfile))
    show_progress(0)
    prog.write_program(hexfile,set_progress=show_progress, config=config, legs=legs)
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
