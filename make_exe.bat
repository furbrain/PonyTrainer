pyupdater build -D -pyinstaller-log-info --app-version %APPVEYOR_BUILD_VERSION% windows.spec
pyupdater pkg -p -s
