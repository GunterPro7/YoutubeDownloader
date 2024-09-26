# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import glob
import os
from PyInstaller.utils.hooks import collect_data_files
resource_dir = '_internal/resources'

# Use glob to find all PNG files in the resources directory
image_files = glob.glob(os.path.join(resource_dir, '*.png'))

# Prepare the datas argument for PyInstaller
datas = [(file, '_internal/resources') for file in image_files]
print(datas)
datas.append(('_internal/ffmpeg.exe', '_internal'))
print(datas)

a = Analysis(
    ['src\\gunterpro7\\main\\main.py'],
    pathex=['src'],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
