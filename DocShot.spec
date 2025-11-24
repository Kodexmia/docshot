# -*- mode: python ; coding: utf-8 -*-
# DocShot v3.6.2 PyInstaller Specification

import os
import sys

block_cipher = None

a = Analysis(
    ['app/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('app/core/_templates', 'app/core/_templates'),
        ('VERSION', '.'),
    ],
    hiddenimports=[
        'PIL',
        'PIL._imaging',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'markdown',
        'jinja2',
        'pydantic',
        'pydantic.dataclasses',
        'pydantic_core',
        'mss',
        'mss.windows',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'pyqthotkey',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'tkinter',
        'unittest',
        'xml',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DocShot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version_file=None,
)
