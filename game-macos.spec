# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
('images/*.png', 'images'),
('images/food/*.png', 'images/food'),
('maps/*.txt', 'maps'),
('fonts/*.ttf', 'fonts'),
]

a = Analysis(['game.py'],
             pathex=['C:\\Users\\Brandon\\Documents\\GitHub\\food-wars'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='game',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )

  app = BUNDLE(exe,
                name='game.app',
                icon=None,
                bundle_identifier=None)
