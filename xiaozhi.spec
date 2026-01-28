# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for 小智 AI Assistant
Target: Windows x64
"""

import os
import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_all, collect_submodules, collect_data_files

# 收集完整的模块（包括数据文件和子模块）
def collect_pkg(package):
    datas, binaries, hiddenimports = collect_all(package)
    return datas, binaries, hiddenimports

# 需要完整收集的包（这些包可能有复杂的子模块或数据文件）
packages_to_collect = [
    # 日志和终端
    'colorlog',
    'rich',
    
    # 日期时间
    'pendulum',
    'dateutil',
    'python_dateutil',
    
    # 网络相关
    'aiohttp',
    'websockets',
    'requests',
    'urllib3',
    
    # AI/API
    'openai',
    
    # 输入设备
    'pynput',
    
    # 音频
    'sounddevice',
    'pygame',
    'mutagen',
    
    # 图像
    'PIL',
    'cv2',
    
    # 加密
    'cryptography',
    
    # 系统
    'psutil',
    'machineid',
    
    # 中文处理
    'pypinyin',
    'lunar_python',
    
    # 解析
    'bs4',
    'beautifulsoup4',
    
    # 压缩
    'brotli',
    
    # Qt 异步
    'qasync',
    
    # MQTT
    'paho',
    'paho.mqtt',
    
    # sherpa-onnx (语音识别)
    'sherpa_onnx',
    
    # 剪贴板
    'pyperclip',
]

collected_datas = []
collected_binaries = []
collected_hiddenimports = []

for pkg in packages_to_collect:
    try:
        d, b, h = collect_pkg(pkg)
        collected_datas.extend(d)
        collected_binaries.extend(b)
        collected_hiddenimports.extend(h)
    except Exception:
        pass

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
    # ==================== 日志 ====================
    "logging",
    "logging.handlers",
    "colorlog",
    "colorlog.colorlog",
    "colorlog.escape_codes",
    
    # ==================== PyQt5 相关 ====================
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
    "sip",
    
    # ==================== qasync ====================
    "qasync",
    "qasync._QEventLoop",
    
    # ==================== 音频相关 ====================
    "sounddevice",
    "_sounddevice_data",
    "pygame",
    "pygame.mixer",
    "pygame.locals",
    "opuslib",
    "opuslib.api",
    "opuslib.api.decoder",
    "opuslib.api.encoder",
    "webrtcvad",
    "soxr",
    "mutagen",
    "mutagen.mp3",
    "mutagen.id3",
    "mutagen.flac",
    
    # ==================== 系统相关 (Windows) ====================
    "comtypes",
    "comtypes.client",
    "comtypes.stream",
    "pycaw",
    "pycaw.pycaw",
    "pycaw.utils",
    "win32api",
    "win32con",
    "win32gui",
    "win32process",
    "win32com",
    "win32com.client",
    "win32com.shell",
    "win32event",
    "win32file",
    "win32pipe",
    "win32security",
    "winerror",
    "pythoncom",
    "pywintypes",
    "winreg",
    
    # ==================== AI/ML 相关 ====================
    "sherpa_onnx",
    "onnxruntime",
    "numpy",
    "numpy.core",
    "numpy.core._methods",
    "numpy.lib",
    "numpy.lib.format",
    "cv2",
    "PIL",
    "PIL.Image",
    "PIL.ImageDraw",
    "PIL.ImageFont",
    
    # ==================== 网络相关 ====================
    "aiohttp",
    "aiohttp.web",
    "aiohttp.client",
    "aiohttp.connector",
    "aiofiles",
    "websockets",
    "websockets.client",
    "websockets.server",
    "websockets.legacy",
    "websockets.legacy.client",
    "paho",
    "paho.mqtt",
    "paho.mqtt.client",
    "paho.mqtt.publish",
    "paho.mqtt.subscribe",
    "requests",
    "requests.adapters",
    "urllib3",
    "urllib3.util",
    "certifi",
    "charset_normalizer",
    "idna",
    
    # ==================== 加密 ====================
    "cryptography",
    "cryptography.fernet",
    "cryptography.hazmat",
    "cryptography.hazmat.backends",
    "cryptography.hazmat.backends.openssl",
    "cryptography.hazmat.primitives",
    "cryptography.hazmat.primitives.ciphers",
    "cryptography.hazmat.primitives.ciphers.algorithms",
    "cryptography.hazmat.primitives.ciphers.modes",
    "cryptography.hazmat.primitives.hashes",
    "cryptography.hazmat.primitives.kdf",
    "_cffi_backend",
    
    # ==================== 日期时间 ====================
    "pendulum",
    "pendulum.locales",
    "pendulum.parsing",
    "pendulum.tz",
    "dateutil",
    "dateutil.parser",
    "dateutil.tz",
    "dateutil.relativedelta",
    "pytz",
    "tzdata",
    
    # ==================== 中文处理 ====================
    "pypinyin",
    "pypinyin.core",
    "pypinyin.style",
    "pypinyin.contrib",
    "lunar_python",
    
    # ==================== 解析 ====================
    "bs4",
    "bs4.builder",
    "beautifulsoup4",
    "html.parser",
    "lxml",
    
    # ==================== 压缩 ====================
    "brotli",
    "_brotli",
    
    # ==================== 终端美化 ====================
    "rich",
    "rich.console",
    "rich.text",
    "rich.table",
    "rich.progress",
    "rich.traceback",
    "rich.markup",
    "rich._palettes",
    "pygments",
    "pygments.lexers",
    "pygments.styles",
    
    # ==================== 输入设备 ====================
    "pynput",
    "pynput.keyboard",
    "pynput.keyboard._win32",
    "pynput.mouse",
    "pynput.mouse._win32",
    "pynput._util",
    "pynput._util.win32",
    
    # ==================== 其他工具 ====================
    "pyperclip",
    "psutil",
    "psutil._pswindows",
    "machineid",
    "packaging",
    "packaging.version",
    "packaging.specifiers",
    "json",
    "uuid",
    "ssl",
    "socket",
    "asyncio",
    "asyncio.events",
    "asyncio.base_events",
    "asyncio.windows_events",
    "concurrent",
    "concurrent.futures",
    "multiprocessing",
    "webbrowser",
    "ctypes",
    "ctypes.wintypes",
    
    # ==================== OpenAI ====================
    "openai",
    "openai.api_resources",
    "httpx",
    "httpcore",
    "anyio",
    "sniffio",
    "h11",
    "httpx._transports",
    "distro",
    "tqdm",
    "tiktoken",
    
    # ==================== 项目模块 ====================
    "src",
    "src.application",
    "src.utils",
    "src.utils.config_manager",
    "src.utils.logging_config",
    "src.utils.resource_finder",
    "src.utils.audio_utils",
    "src.utils.common_utils",
    "src.utils.device_activator",
    "src.utils.device_fingerprint",
    "src.utils.opus_loader",
    "src.utils.volume_controller",
    "src.core",
    "src.core.ota",
    "src.core.system_initializer",
    "src.display",
    "src.display.base_display",
    "src.display.cli_display",
    "src.display.gui_display",
    "src.display.gui_display_model",
    "src.plugins",
    "src.plugins.audio",
    "src.plugins.base",
    "src.plugins.manager",
    "src.protocols",
    "src.protocols.protocol",
    "src.protocols.websocket_protocol",
    "src.protocols.mqtt_protocol",
    "src.audio_codecs",
    "src.audio_codecs.audio_codec",
    "src.audio_codecs.music_decoder",
    "src.audio_codecs.aec_processor",
    "src.audio_processing",
    "src.audio_processing.wake_word_detect",
    "src.iot",
    "src.iot.thing",
    "src.iot.thing_manager",
    "src.mcp",
    "src.mcp.mcp_server",
    "src.network",
    "src.network.mqtt_client",
    "src.views",
    "src.views.base",
    "src.views.activation",
    "src.views.settings",
    "src.views.components",
    "src.constants",
    "src.constants.constants",
    "src.constants.system",
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

# 合并收集的数据
datas = datas + collected_datas
binaries = binaries + collected_binaries
hiddenimports = hiddenimports + collected_hiddenimports

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
