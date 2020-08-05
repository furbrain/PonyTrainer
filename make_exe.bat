#!/bin/sh
VERSION=`git describe --tags`
pyupdater build --app-version 1.0.0  --add-binary="libusb-1.0.dll;." --add-data="doc/manual.pdf;." --onefile PonyTrainer.py
pyupdater pkg -p -s
