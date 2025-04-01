# AiAmy.spec
# -*- mode: python ; coding: utf-8 -*-

import os
# --- Import the library to find its path ---
import llama_cpp  # Make sure llama-cpp-python is installed in your .venv

spec_root = os.getcwd()
print(f"INFO: Using project root (spec_root): {spec_root}")

# --- Find the llama_cpp installation path ---
try:
    llama_cpp_pkg_dir = os.path.dirname(llama_cpp.__file__)
    # --- Construct the path to the crucial 'lib' directory within llama_cpp ---
    # This often contains the core DLLs/SOs needed at runtime.
    source_llama_lib_dir = os.path.join(llama_cpp_pkg_dir, 'lib')
    print(f"INFO: Trying to find llama_cpp 'lib' source directory at: {source_llama_lib_dir}")
    if not os.path.isdir(source_llama_lib_dir):
         print(f"WARNING: Standard 'lib' directory not found in llama_cpp package.")
         # Sometimes binaries are directly in the package root or another subdir
         # If the above fails, you might need to adjust 'lib' or look inside llama_cpp_pkg_dir
         # For now, we proceed assuming 'lib' is correct or the hook handles it partially.
         source_llama_lib_dir = None # Set to None if not found, to avoid error below
except ImportError:
    print("ERROR: llama_cpp package not found. Cannot determine binary paths.")
    llama_cpp_pkg_dir = None
    source_llama_lib_dir = None

# --- Define SOURCE paths for your app's files/folders ---
source_config = os.path.join(spec_root, 'config.yml')
source_log_folder = os.path.join(spec_root, 'logs')
source_chars_folder = os.path.join(spec_root, 'chars')

# --- Define the datas list for PyInstaller ---
app_datas = [
    (source_config, '.'),
    (source_log_folder, 'logs'),
    (source_chars_folder, 'chars'),
]

# --- Add the llama_cpp lib directory MANUALLY to datas ---
if source_llama_lib_dir and os.path.isdir(source_llama_lib_dir):
    # The destination 'llama_cpp/lib' tells PyInstaller to put it
    # inside the bundled llama_cpp package structure (_internal/llama_cpp/lib).
    app_datas.append((source_llama_lib_dir, 'llama_cpp/lib'))
    print(f"INFO: Adding llama_cpp lib directory to datas: {source_llama_lib_dir} -> llama_cpp/lib")
else:
    print(f"WARNING: Not adding llama_cpp lib directory to datas as source path was not found.")


# Filter out non-existent source paths from datas to avoid PyInstaller errors
app_datas = [(src, dst) for src, dst in app_datas if os.path.exists(src)]
print(f"INFO: Final datas list for bundling: {app_datas}")


# --- Define binaries list (e.g., for tbb12.dll if needed later) ---
# Leave empty for now, focus on llama_cpp first
app_binaries = []
# app_binaries = [(src, dst) for src, dst in app_binaries if os.path.exists(src)]


a = Analysis(
    # --- Using main.py as entry point again ---
    ['src/ai_amy/main.py'],
    pathex=[os.path.join(spec_root, 'src')], # Keep src in pathex
    binaries=app_binaries,           # Pass binaries list (currently empty)
    datas=app_datas,                 # <--- Pass the UPDATED datas list
    hiddenimports=[],
    hookspath=[],                    # You can leave hooks-contrib installed, it just wasn't sufficient
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
    name='AiAmy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # Or False
    # ... rest of EXE definition ...
)

coll = COLLECT(
    exe,
    a.binaries,                     # Make sure binaries are collected (even if empty now)
    a.datas,                        # Make sure datas are collected
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AiAmy',
)