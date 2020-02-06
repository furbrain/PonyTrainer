#!/bin/sh
VERSION=`git describe --tags`
echo "VERSION=\"$VERSION\"" > PonyTrainer/version.py
pyinstaller \
  --add-data="doc/manual.pdf:." \
  --noconfirm \
  --onefile \
  --name "PonyTrainer-$VERSION-linux.run" \
  PonyTrainer/PonyTrainer.py
