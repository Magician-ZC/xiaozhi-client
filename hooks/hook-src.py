# PyInstaller hook for src package
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('src')
datas = collect_data_files('src', include_py_files=True)
