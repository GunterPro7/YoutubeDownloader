# -*- mode: python ; coding: utf-8 -*-
import glob
import os
from PyInstaller.utils.hooks import collect_data_files
resource_dir = '_internal/resources'

# Use glob to find all PNG files in the resources directory
image_files = glob.glob(os.path.join(resource_dir, '*.png'))

# Prepare the datas argument for PyInstaller
datas = [(file, 'resources') for file in image_files]
print(datas)
datas.append(('_internal/ffmpeg.exe', '.'))
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
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='YouTubeToMp3',
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
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
