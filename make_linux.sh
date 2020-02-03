#!/bin/sh
pyinstaller \
  --add-data="doc/manual.pdf:." \
  --noconfirm \
  --onefile \
  PonyTrainer/PonyTrainer.py
