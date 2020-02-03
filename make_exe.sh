#!/bin/sh
wine ~/.wine/drive_c/Python38/Scripts/pyinstaller.exe \
  --add-binary="libusb-1.0.dll;." \
  --add-data="doc/manual.pdf;." \
  --noconfirm \
  --onefile \
  PonyTrainer/PonyTrainer.py
