pyupdater build --app-version %APPVEYOR_BUILD_VERSION% windows.spec
pyupdater pkg -p -s
