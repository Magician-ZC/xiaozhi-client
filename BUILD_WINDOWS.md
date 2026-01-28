# Windows 打包指南

本文档说明如何将小智 AI 客户端打包成 Windows 可执行程序。

## 方案选择

| 方案 | 适用场景 | 是否需要 Windows |
|------|----------|------------------|
| GitHub Actions | 推荐，适合大多数情况 | ❌ 不需要 |
| 本地打包 | 需要调试或自定义 | ✅ 需要 |

---

## 方案一：GitHub Actions 自动打包（推荐）

无需 Windows 电脑，推送代码到 GitHub 后自动在云端打包。

### 使用方法

**方法 A：手动触发**

1. 进入 GitHub 仓库页面
2. 点击 **Actions** 标签
3. 选择 **Build Windows** 工作流
4. 点击 **Run workflow** 按钮
5. 可选填写版本号，点击绿色按钮运行
6. 等待几分钟，完成后在 **Artifacts** 下载 ZIP 文件

**方法 B：通过 Tag 触发**

```bash
# 创建并推送 tag
git tag v1.1.9
git push origin v1.1.9
```

推送 tag 后会自动打包，完成后在 GitHub Releases 页面下载。

---

## 方案二：本地打包

如果需要在 Windows 电脑上本地打包，请参考以下步骤。

## 环境要求

- **操作系统**: Windows 10/11 (64位)
- **Python**: 3.9 - 3.11 (推荐 3.10)
- **磁盘空间**: 至少 2GB 可用空间

## 快速开始

### 方法一：使用批处理脚本（推荐）

1. 双击运行 `build_windows.bat`
2. 脚本会自动：
   - 创建虚拟环境
   - 安装依赖
   - 转换图标格式
   - 执行打包
3. 打包完成后，可执行文件位于 `dist\小智\` 目录

### 方法二：使用 Python 脚本

```bash
# 安装依赖
pip install -r requirements.txt

# 执行打包
python build_app.py

# 或者清理后打包
python build_app.py --clean

# 使用 spec 文件打包（更可控）
python build_app.py --spec
```

### 方法三：手动执行 PyInstaller

```bash
# 安装依赖
pip install -r requirements.txt

# 使用 spec 文件打包
pyinstaller xiaozhi.spec --clean --noconfirm
```

## 打包产物

打包完成后，文件结构如下：

```
dist/
└── 小智/
    ├── 小智.exe          # 主程序
    ├── _internal/        # Python 运行时和依赖
    ├── assets/           # 图标、表情等资源
    ├── config/           # 配置文件
    ├── libs/             # 动态库
    ├── models/           # AI 模型文件
    ├── scripts/          # 脚本
    └── src/              # 源代码和 QML 文件
```

## 运行程序

直接双击 `dist\小智\小智.exe` 即可运行。

**注意**：首次运行时可能会触发 Windows 安全警告，点击「仍要运行」即可。

## 分发

可以将整个 `dist\小智\` 文件夹压缩后分发给其他用户。

如需制作安装程序，可以使用：
- [Inno Setup](https://jrsoftware.org/isinfo.php) - 免费的安装程序制作工具
- [NSIS](https://nsis.sourceforge.io/) - 另一个流行的安装程序制作工具

## 常见问题

### 1. 打包失败：找不到模块

确保所有依赖已正确安装：
```bash
pip install -r requirements.txt
```

### 2. 程序启动后立即闪退

可能是缺少 Visual C++ 运行库。请安装：
- [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### 3. 提示缺少 DLL 文件

确保 `libs` 目录中的 DLL 文件已正确打包。检查：
- `libs/libopus/win/x64/opus.dll`
- `libs/webrtc_apm/windows/x64/libwebrtc_apm.dll`

### 4. 图标显示不正确

确保 `assets/icon.ico` 文件存在。如果只有 PNG 格式：
```python
# 转换图标
pip install pillow
python -c "from PIL import Image; img = Image.open('assets/icon.png'); img.save('assets/icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])"
```

### 5. 打包体积过大

打包后体积较大是正常的（通常 200-500MB），因为包含了：
- Python 运行时
- PyQt5 库
- AI 模型文件
- 各种依赖库

如需减小体积，可以：
1. 使用 UPX 压缩（已默认启用）
2. 排除不需要的模块
3. 使用虚拟环境，只安装必要依赖

### 6. 杀毒软件误报

PyInstaller 打包的程序有时会被杀毒软件误报。解决方案：
1. 将程序添加到杀毒软件白名单
2. 使用代码签名证书签名程序

## 高级配置

### 修改 spec 文件

`xiaozhi.spec` 文件包含了详细的打包配置，可以根据需要修改：

- `hiddenimports`: 添加需要的隐藏导入模块
- `datas`: 添加需要打包的数据文件
- `excludes`: 排除不需要的模块
- `console`: 设为 `True` 可显示控制台窗口（用于调试）

### 添加版本信息

创建 `version_info.txt` 文件并在 spec 中引用，可以在 exe 属性中显示版本信息。

## 技术支持

如遇到问题，请提交 Issue 并附上：
1. 错误日志
2. Python 版本
3. Windows 版本
4. 依赖安装情况
