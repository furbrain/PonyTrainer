#!/bin/sh
VERSION=`git describe --tags`
pyupdater make-spec \
  --add-data="doc/manual.pdf:." \
  --onefile \
  --name "PonyTrainer-$VERSION-linux.run" \
  --paths "src" \
  src/PonyTrainer.py
