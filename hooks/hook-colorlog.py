# PyInstaller hook for colorlog
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('colorlog')
