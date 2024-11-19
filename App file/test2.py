# Import PyInstaller modules
# -*- mode: python ; coding: utf-8 -*-

# Imports necessary modules
block_cipher = None

# Analysis section where all modules, data, and dependencies are specified
a = Analysis(
    ['app.py'],  # Main script
    pathex=['path/to/your/project'],  # Adjust path to your project folder
    binaries=[],  # List binaries if there are any
    datas=[('storedatabase.db', '.')],  # Includes the database file
    hiddenimports=['cart', 'product_list', 'SeeActivity'],  # Include other Python files
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

# PyInstaller bundles all files into a single package
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Creates an executable based on the analysis
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='StoreManagementApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Change to True if you want a console window to show
    icon='path/to/your/icon.ico'  # Optional: specify an icon file if desired
)

# Collates everything into a single directory for distribution
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='StoreManagementApp'
)
