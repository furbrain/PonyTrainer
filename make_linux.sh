#!/bin/sh
VERSION=`git describe --tags`
pyupdater build --app-version $VERSION linux.spec
pyupdater pkg -p -s
