# -*- mode: python -*-
a = Analysis(['Systeembord.py'],
             pathex=['C:\\Users\\Pieter\\CloudStation\\GIT projecten no sync\\Systeembord'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
Tree('C:\\Users\\Pieter\\CloudStation\\GIT projecten no sync\\Systeembord\\Items', prefix="Items\\"),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Systeembord.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
