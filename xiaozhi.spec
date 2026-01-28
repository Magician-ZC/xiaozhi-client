# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for 小智 AI Assistant
Target: Windows x64
"""

import os
import sys
from pathlib import Path

# 获取项目根目录
project_root = Path(SPECPATH).resolve()

# 应用信息
APP_NAME = "小智"
APP_VERSION = "1.1.9"
MAIN_SCRIPT = "main.py"

# 图标路径（Windows需要.ico格式）
icon_path = project_root / "assets" / "icon.ico"
if not icon_path.exists():
    # 如果没有.ico，尝试使用.png（PyInstaller会自动转换）
    icon_path = project_root / "assets" / "icon.png"
    if not icon_path.exists():
        icon_path = None

# 数据文件收集
datas = [
    # 模型文件
    (str(project_root / "models"), "models"),
    # 脚本
    (str(project_root / "scripts"), "scripts"),
    # 源代码（包含QML等资源）
    (str(project_root / "src"), "src"),
    # 动态库
    (str(project_root / "libs"), "libs"),
    # 资源文件（图标、表情等）
    (str(project_root / "assets"), "assets"),
    # 配置文件
    (str(project_root / "config"), "config"),
]

# 过滤掉不存在的路径
datas = [(src, dst) for src, dst in datas if Path(src).exists()]

# 隐藏导入 - 确保所有需要的模块都被包含
hiddenimports = [
    # PyQt5 相关
    "PyQt5",
    "PyQt5.QtCore",
    "PyQt5.QtGui",
    "PyQt5.QtWidgets",
    "PyQt5.QtQml",
    "PyQt5.QtQuick",
    "PyQt5.QtQuickWidgets",
    "PyQt5.QtNetwork",
    "PyQt5.QtMultimedia",
    "PyQt5.sip",
    
    # qasync
    "qasync",
    
    # 音频相关
    "sounddevice",
    "pygame",
    "pygame.mixer",
    "opuslib",
    "webrtcvad",
    "soxr",
    
    # 系统相关 (Windows)
    "comtypes",
    "comtypes.client",
    "pycaw",
    "pycaw.pycaw",
    "win32api",
    "win32con",
    "win32gui",
    "win32process",
    "win32com",
    "win32com.client",
    "pythoncom",
    "pywintypes",
    
    # AI/ML 相关
    "sherpa_onnx",
    "onnxruntime",
    "numpy",
    "cv2",
    
    # 网络相关
    "aiohttp",
    "websockets",
    "paho.mqtt",
    "paho.mqtt.client",
    "requests",
    
    # 加密
    "cryptography",
    "cryptography.fernet",
    
    # 其他
    "PIL",
    "PIL.Image",
    "pendulum",
    "mutagen",
    "bs4",
    "colorlog",
    "rich",
    "pynput",
    "pynput.keyboard",
    "pynput.mouse",
    "pyperclip",
    "pypinyin",
    "psutil",
    "packaging",
    "dateutil",
    "lunar_python",
    "brotli",
    
    # 项目模块
    "src",
    "src.application",
    "src.utils",
    "src.utils.config_manager",
    "src.utils.logging_config",
    "src.utils.resource_finder",
    "src.core",
    "src.display",
    "src.plugins",
    "src.protocols",
    "src.audio_codecs",
    "src.audio_processing",
    "src.iot",
    "src.mcp",
    "src.network",
    "src.views",
    "src.constants",
]

# 排除不需要的模块（减小体积）
excludes = [
    "tkinter",
    "matplotlib",
    "scipy",
    "pandas",
    "IPython",
    "jupyter",
    "notebook",
    "test",
    "tests",
    "unittest",
    "pytest",
]

# 运行时钩子
runtime_hooks = []

# 二进制文件收集
binaries = []

# Windows 特定的 DLL
if sys.platform == "win32":
    # opus.dll
    opus_dll = project_root / "libs" / "libopus" / "win" / "x64" / "opus.dll"
    if opus_dll.exists():
        binaries.append((str(opus_dll), "."))
    
    # webrtc_apm DLL
    webrtc_dll = project_root / "libs" / "webrtc_apm" / "windows" / "x64" / "libwebrtc_apm.dll"
    if webrtc_dll.exists():
        binaries.append((str(webrtc_dll), "."))

# Analysis
a = Analysis(
    [MAIN_SCRIPT],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=runtime_hooks,
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# PYZ - Python 字节码压缩包
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# EXE - 可执行文件
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,  # onedir 模式
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # windowed 模式，不显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(icon_path) if icon_path else None,
    version_info=None,  # 可以添加版本信息文件
)

# COLLECT - 收集所有文件到一个目录
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)
