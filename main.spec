# -*- mode: python ; coding: utf-8 -*-

import os
import sys
# Import llama_cpp to find its installation path
try:
    import llama_cpp
    # Construct the source path for the 'lib' directory containing the shared libraries
    # This assumes the compiled libraries are directly in a 'lib' subdir of the package
    llama_cpp_lib_path = os.path.join(os.path.dirname(llama_cpp.__file__), 'lib')

    # Check if the path actually exists, handle potential variations if needed
    if not os.path.isdir(llama_cpp_lib_path):
        # Some builds might place it elsewhere, e.g., directly in the package root or vendor
        # Adjust this path if the 'lib' folder isn't found directly under llama_cpp
        # Example fallback (check package root):
        # llama_cpp_lib_path = os.path.dirname(llama_cpp.__file__)
        # Or check a 'vendor' directory if applicable based on your llama-cpp-python build
        # llama_cpp_lib_path = os.path.join(os.path.dirname(llama_cpp.__file__), 'vendor') # Example

        # If still not found, raise a more informative error
        if not os.path.isdir(llama_cpp_lib_path):
             raise FileNotFoundError(f"Could not automatically find the llama_cpp native library directory. Looked in: {os.path.join(os.path.dirname(llama_cpp.__file__), 'lib')}")

    # Define the data tuple for PyInstaller
    llama_datas = [(llama_cpp_lib_path, '_internal/llama_cpp/lib')]
    print(f"INFO: Adding llama_cpp library data: {llama_datas}")

except ImportError:
    print("WARNING: llama_cpp not found in the build environment. Cannot automatically package its libraries.", file=sys.stderr)
    llama_datas = []
except FileNotFoundError as e:
    print(f"ERROR: {e}", file=sys.stderr)
    print("Please verify the structure of your installed 'llama-cpp-python' package and adjust the path in the spec file.", file=sys.stderr)
    sys.exit(1)


a = Analysis(
    ['src\\ai_amy\\main.py'],
    pathex=[],
    binaries=[],
    # Add the llama_cpp lib directory to datas
    datas=llama_datas,
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
    # Make sure datas collected by Analysis are included in the final bundle
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)