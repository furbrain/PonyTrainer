#!/bin/sh
pyupdater build --app-version $APPVEYOR_BUILD_VERSION linux.spec
pyupdater pkg -p -s
