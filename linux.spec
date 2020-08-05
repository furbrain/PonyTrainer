# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['./PonyTrainer.py'],
             pathex=['.', '/home/appveyor/venv3.6/lib/python3.6/site-packages'],
             binaries=[],
             datas=[('doc/manual.pdf', '.')],
             hiddenimports=[],
             hookspath=['/usr/local/lib/python3.6/dist-packages/pyupdater/hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='nix64',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='nix64')
