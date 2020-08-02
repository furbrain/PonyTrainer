#!/bin/sh
VERSION=`git describe --tags`
echo "VERSION=\"$VERSION\"" > PonyTrainer/version.py
wine ~/.wine/drive_c/Python38/Scripts/pyupdater.exe build \
  --app-version=$VERSION \
  --add-binary="libusb-1.0.dll;." \
  --add-data="doc/manual.pdf;." \
  --noconfirm \
  --onefile \
  --name "PonyTrainer-$VERSION.exe" \
  src/PonyTrainer.py
