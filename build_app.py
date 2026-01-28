#!/usr/bin/env python3
"""
小智 AI 客户端 - 跨平台打包脚本
支持 Windows、macOS、Linux

用法:
    python build_app.py              # 自动检测平台并打包
    python build_app.py --clean      # 清理后打包
    python build_app.py --onefile    # 打包成单文件（不推荐）
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.resolve()

# 从 build.json 读取配置
BUILD_CONFIG_PATH = PROJECT_ROOT / "build.json"


def load_build_config() -> dict:
    """加载构建配置"""
    if BUILD_CONFIG_PATH.exists():
        with open(BUILD_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_platform_info() -> tuple:
    """获取平台信息"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "darwin":
        platform_name = "macos"
    elif system == "windows":
        platform_name = "windows"
    else:
        platform_name = "linux"
    
    if machine in ("x86_64", "amd64"):
        arch = "x64"
    elif machine in ("arm64", "aarch64"):
        arch = "arm64"
    else:
        arch = machine
    
    return platform_name, arch


def ensure_icon(config: dict) -> Path | None:
    """确保图标文件存在且格式正确"""
    icon_path = PROJECT_ROOT / config.get("icon", "assets/icon.png")
    
    if platform.system() == "Windows":
        ico_path = icon_path.with_suffix(".ico")
        if not ico_path.exists() and icon_path.exists():
            print("[信息] 转换图标为 ICO 格式...")
            try:
                from PIL import Image
                img = Image.open(icon_path)
                # Windows 图标需要多种尺寸
                sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                img.save(ico_path, format="ICO", sizes=sizes)
                print(f"[信息] 图标已保存到: {ico_path}")
            except ImportError:
                print("[警告] 需要 Pillow 库来转换图标: pip install pillow")
                return icon_path if icon_path.exists() else None
            except Exception as e:
                print(f"[警告] 图标转换失败: {e}")
                return icon_path if icon_path.exists() else None
        return ico_path if ico_path.exists() else icon_path if icon_path.exists() else None
    elif platform.system() == "Darwin":
        icns_path = icon_path.with_suffix(".icns")
        return icns_path if icns_path.exists() else icon_path if icon_path.exists() else None
    else:
        return icon_path if icon_path.exists() else None


def build_pyinstaller_args(config: dict, onefile: bool = False) -> list:
    """构建 PyInstaller 命令参数"""
    args = ["pyinstaller"]
    
    # 基本配置
    pi_config = config.get("pyinstaller", {})
    platform_name, _ = get_platform_info()
    platform_config = config.get("platforms", {}).get(platform_name, {}).get("pyinstaller", {})
    
    # 合并平台特定配置
    pi_config.update(platform_config)
    
    # 入口文件
    entry = config.get("entry", "main.py")
    
    # 应用名称
    name = config.get("name", "小智")
    args.extend(["--name", name])
    
    # 图标
    icon = ensure_icon(config)
    if icon:
        args.extend(["--icon", str(icon)])
    
    # 单文件或目录模式
    if onefile or pi_config.get("onefile", False):
        args.append("--onefile")
    else:
        args.append("--onedir")
    
    # 窗口模式
    if pi_config.get("windowed", True):
        args.append("--windowed")
    
    # 数据文件
    add_data = pi_config.get("add_data", [])
    # 默认数据文件
    default_data = ["models:models", "scripts:scripts", "src:src", "libs:libs", "assets:assets", "config:config"]
    for item in default_data:
        if item not in add_data:
            add_data.append(item)
    
    separator = ";" if platform.system() == "Windows" else ":"
    for data in add_data:
        src, dst = data.split(":")
        src_path = PROJECT_ROOT / src
        if src_path.exists():
            args.extend(["--add-data", f"{src_path}{separator}{dst}"])
    
    # 隐藏导入
    hidden_imports = [
        # PyQt5
        "PyQt5", "PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets",
        "PyQt5.QtQml", "PyQt5.QtQuick", "PyQt5.QtQuickWidgets", "PyQt5.sip",
        # qasync
        "qasync",
        # 音频
        "sounddevice", "pygame", "pygame.mixer", "opuslib", "webrtcvad", "soxr",
        # AI/ML
        "sherpa_onnx", "onnxruntime", "numpy", "cv2",
        # 网络
        "aiohttp", "websockets", "paho.mqtt", "paho.mqtt.client", "requests",
        # 加密
        "cryptography", "cryptography.fernet",
        # 其他
        "PIL", "PIL.Image", "pendulum", "mutagen", "bs4", "colorlog", "rich",
        "pynput", "pynput.keyboard", "pynput.mouse", "pyperclip", "pypinyin",
        "psutil", "packaging", "dateutil", "lunar_python", "brotli",
    ]
    
    # Windows 特定
    if platform.system() == "Windows":
        hidden_imports.extend([
            "comtypes", "comtypes.client", "pycaw", "pycaw.pycaw",
            "win32api", "win32con", "win32gui", "win32process",
            "win32com", "win32com.client", "pythoncom", "pywintypes",
        ])
    
    for imp in hidden_imports:
        args.extend(["--hidden-import", imp])
    
    # 排除
    excludes = ["tkinter", "matplotlib", "scipy", "pandas", "IPython", "jupyter", "notebook"]
    for exc in excludes:
        args.extend(["--exclude-module", exc])
    
    # 其他选项
    if pi_config.get("clean", True):
        args.append("--clean")
    if pi_config.get("noconfirm", True):
        args.append("--noconfirm")
    
    # 路径
    args.extend(["--paths", str(PROJECT_ROOT)])
    
    # 工作目录和输出目录
    args.extend(["--workpath", str(PROJECT_ROOT / "build")])
    args.extend(["--distpath", str(PROJECT_ROOT / "dist")])
    args.extend(["--specpath", str(PROJECT_ROOT)])
    
    # 入口文件
    args.append(str(PROJECT_ROOT / entry))
    
    return args


def clean_build():
    """清理构建目录"""
    print("[信息] 清理构建目录...")
    for dir_name in ["build", "dist"]:
        dir_path = PROJECT_ROOT / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  - 已删除: {dir_path}")


def check_dependencies():
    """检查依赖"""
    print("[信息] 检查依赖...")
    
    # 检查 PyInstaller
    try:
        import PyInstaller
        print(f"  - PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("[错误] 未安装 PyInstaller，请运行: pip install pyinstaller")
        return False
    
    # 检查 PyQt5
    try:
        from PyQt5.QtCore import QT_VERSION_STR
        print(f"  - PyQt5: {QT_VERSION_STR}")
    except ImportError:
        print("[警告] 未安装 PyQt5")
    
    return True


def run_build(args: list):
    """执行打包"""
    print("\n[信息] 开始打包...")
    print(f"  命令: {' '.join(args[:5])}...")
    print("-" * 50)
    
    result = subprocess.run(args, cwd=PROJECT_ROOT)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="小智 AI 客户端打包脚本")
    parser.add_argument("--clean", action="store_true", help="清理后打包")
    parser.add_argument("--onefile", action="store_true", help="打包成单文件")
    parser.add_argument("--spec", action="store_true", help="使用 spec 文件打包")
    args = parser.parse_args()
    
    print("=" * 50)
    print("    小智 AI 客户端 - 打包脚本")
    print("=" * 50)
    
    platform_name, arch = get_platform_info()
    print(f"\n[信息] 平台: {platform_name} ({arch})")
    print(f"[信息] Python: {sys.version.split()[0]}")
    
    # 加载配置
    config = load_build_config()
    print(f"[信息] 应用: {config.get('name', '小智')} v{config.get('version', '1.0.0')}")
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    # 清理
    if args.clean:
        clean_build()
    
    # 构建
    if args.spec:
        spec_file = PROJECT_ROOT / "xiaozhi.spec"
        if spec_file.exists():
            build_args = ["pyinstaller", str(spec_file), "--clean", "--noconfirm"]
        else:
            print(f"[错误] 未找到 spec 文件: {spec_file}")
            return 1
    else:
        build_args = build_pyinstaller_args(config, args.onefile)
    
    success = run_build(build_args)
    
    if success:
        print("\n" + "=" * 50)
        print("    打包完成！")
        print("=" * 50)
        
        dist_dir = PROJECT_ROOT / "dist" / config.get("name", "小智")
        if dist_dir.exists():
            print(f"\n输出目录: {dist_dir}")
            
            # 显示可执行文件
            if platform.system() == "Windows":
                exe = dist_dir / f"{config.get('name', '小智')}.exe"
            elif platform.system() == "Darwin":
                exe = dist_dir / f"{config.get('name', '小智')}.app"
            else:
                exe = dist_dir / config.get('name', '小智')
            
            if exe.exists():
                print(f"可执行文件: {exe}")
        
        return 0
    else:
        print("\n[错误] 打包失败！")
        return 1


if __name__ == "__main__":
    sys.exit(main())
