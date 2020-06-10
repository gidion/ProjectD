# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('tensorflow_core')
datas = collect_data_files('tensorflow_core', subdir=None, include_py_files=True)
datas += collect_data_files('astor', subdir=None, include_py_files=False)

block_cipher = None


a = Analysis(['C:\\Users\\gerdw\\Documents\\GitHub\\ProjectD\\main.py'],
             pathex=['C:\\Users\\gerdw\\Documents\\GitHub\\ProjectD\\Tashira'],
             binaries=[],
             datas=[],
             hiddenimports=['pkg_resources.py2_warn','win32timezone'],
             hookspath=[],
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
          name='tashira',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True )
coll = COLLECT(exe,Tree('C:\\Users\\gerdw\\Documents\\GitHub\\ProjectD\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='tashira',
               icon='icon.ico')
