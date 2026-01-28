@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo     小智 AI 客户端 - Windows 打包脚本
echo ========================================
echo.

:: 检查 Python 环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

:: 显示 Python 版本
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [信息] 使用 %PYTHON_VERSION%
echo.

:: 检查是否在项目目录
if not exist "main.py" (
    echo [错误] 请在项目根目录运行此脚本
    pause
    exit /b 1
)

:: 检查虚拟环境
if not exist "venv" (
    echo [信息] 创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
)

:: 激活虚拟环境
echo [信息] 激活虚拟环境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [错误] 激活虚拟环境失败
    pause
    exit /b 1
)

:: 安装/更新依赖
echo [信息] 安装依赖包...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [警告] 部分依赖安装可能失败，继续尝试打包...
)

:: 确保 PyInstaller 已安装
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [信息] 安装 PyInstaller...
    pip install pyinstaller
)

:: 检查图标文件
if not exist "assets\icon.ico" (
    echo [信息] 未找到 icon.ico，尝试从 icon.png 转换...
    if exist "assets\icon.png" (
        pip show pillow >nul 2>&1
        if errorlevel 1 pip install pillow
        python -c "from PIL import Image; img = Image.open('assets/icon.png'); img.save('assets/icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])" 2>nul
        if exist "assets\icon.ico" (
            echo [信息] 图标转换成功
        ) else (
            echo [警告] 图标转换失败，将使用默认图标
        )
    )
)

:: 清理旧的构建
echo [信息] 清理旧的构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

:: 开始打包
echo.
echo [信息] 开始打包...
echo ----------------------------------------
pyinstaller xiaozhi.spec --clean --noconfirm
if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo     打包完成！
echo ========================================
echo.
echo 输出目录: dist\小智\
echo 可执行文件: dist\小智\小智.exe
echo.

:: 显示输出目录大小
for /f "tokens=3" %%a in ('dir "dist\小智" /s ^| findstr "个文件"') do set SIZE=%%a
echo 总大小: 约 %SIZE% 字节
echo.

:: 询问是否打开输出目录
set /p OPEN_DIR="是否打开输出目录？(Y/N): "
if /i "%OPEN_DIR%"=="Y" (
    explorer "dist\小智"
)

pause
