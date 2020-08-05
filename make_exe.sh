#!/bin/sh
VERSION=`git describe --tags`
wine ~/.wine/drive_c/Python38/Scripts/pyupdater.exe make-spec \
  --add-binary="libusb-1.0.dll;." \
  --add-data="doc/manual.pdf;." \
  --onefile \
  PonyTrainer.py
