#!/bin/sh
pyupdater build -D -pyinstaller-log-info --app-version $APPVEYOR_BUILD_VERSION linux.spec
pyupdater pkg -p -s
