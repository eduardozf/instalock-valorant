[English](README.md) | [Português](README_PTBR.md) | [中文](README_CN.md)

# Valorant 秒选宏 🎯

一个帮助你在 Valorant 中秒选特工的 Python 脚本。仅供教育目的使用 👀

<div style="display: grid; grid-column: 3;">
    <img src="examples/main_menu.png" alt="Main Menu" style="width: auto; height: 320px; object-fit: contain;"/>
    <img src="examples/record_agent.png" alt="Record Agent" style="width: auto; height: 320px; object-fit: contain;"/>
    <img src="examples/instalock_mode.png" alt="Instalock Mode" style="width: auto; height: 320px; object-fit: contain;"/>
</div>

> [!WARNING]  
> 此工具可能违反 Valorant 的服务条款。使用风险自负。创作者不对任何后果负责。

## 功能特点

- 具有可配置按键的简单特工选择
- 多语言支持（英语、葡萄牙语、中文）
- 简单的设置流程
- 可配置的点击延迟和位置
- 具有可配置误差边距的随机点击位置有助于防止宏被检测
- 增强的错误处理和稳定性
- 直观的菜单界面，提供以下选项：
  - 录制新特工
  - 启动宏监听
  - 刷新设置
  - 解绑特工

## 前置要求

1. **安装 Python**:

   - 从 [python.org](https://python.org/downloads/) 下载 Python
   - 安装时，**务必勾选** "Add Python to PATH"
   - 安装完成后，重启终端/命令提示符 (CMD)

2. **验证 Python 安装**:
   ```bash
   python --version
   ```
   如果看到版本号，说明 Python 安装成功！

## 安装步骤

1. **下载项目**:

   **方式 A - 使用 Git**:

   ```bash
   git clone https://github.com/yourusername/valorant-instalock
   cd valorant-instalock
   ```

   **方式 B - 不使用 Git**:

   - 前往仓库页面
   - 点击绿色的 "Code" 按钮
   - 选择 "Download ZIP"
   - 将 ZIP 文件解压到文件夹（例如桌面）
   - 记住文件夹位置（例如 `C:\Users\YourUser\Desktop\valorant-instalock-main`）

2. **导航到项目文件夹**:

   **方式 A - Windows 11（最简单的方式）**:

   - 进入解压后的文件夹
   - 在文件夹空白处右键点击
   - 选择"在终端中打开"

   **方式 B - 使用命令提示符**:

   - 打开命令提示符 (CMD)
   - 使用 `cd` 命令导航到项目文件夹：

   ```bash
   # 如果解压到桌面：
   cd C:\Users\YourUser\Desktop\valorant-instalock-main

   # 或者直接使用完整路径：
   cd "你的解压文件夹路径"
   ```

3. **安装依赖**:

   确保你在项目文件夹中（有 `requirements.txt` 的位置）并运行：

   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. **游戏设置**:

   - 建议：将 Valorant 设置为"窗口化全屏"模式（便于查看特工位置）
   - 建议：仅在自定义游戏中使用

2. **运行脚本**:

   确保你在项目文件夹中并运行：

   ```bash
   python -m src
   ```

   如果关闭了终端，需要按照上面的**导航到项目文件夹**步骤重新进入。

3. **使用菜单**:

   - 使用方向键导航菜单
   - 按 Enter 选择选项
   - 按 DELETE 解绑特工
   - 按 Ctrl+C 取消或退出

4. **录制特工**:

   - 在菜单中选择"录制新特工"
   - 使用方向键和回车键选择特工
   - 按下你想用于该特工的按键（如 DELETE、END、HOME 等）
   - 将鼠标移动到选择界面上特工出现的位置并按空格
   - 将鼠标移动到确认按钮并按空格

5. **使用宏**:
   - 在菜单中选择"启动宏监听"
   - 当特工选择开始时，*按住*你为目标特工设置的按键
   - 特工锁定后松开按键
   - 按 Esc 返回主菜单，这样宏就不会影响你的操作

## 使用技巧

- 每个特工可以设置独立的按键绑定
- 在任何操作期间按 Ctrl+C 可以取消
- 使用 DELETE 键解绑特工
- 脚本会自动保存你的配置
- **配置文件** (`config.json`):
  - 位于项目文件夹中
  - 简单重置：直接删除 `config.json` 并重新启动脚本
  - 完全可自定义：
    - 手动编辑按键绑定
    - 添加或删除特工配置
    - 在 "delays" 部分调整点击延迟
    - 使用 "margin_of_error" 设置微调检测规避

## 贡献

欢迎提交问题和拉取请求！

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件。

## 教育目的

本项目仅用于教育目的，用于展示：

- Python 自动化功能
- GUI 交互
- 多语言支持
- 配置管理
- 事件处理

请记住：在竞技游戏中使用宏可能导致账号处罚。请负责任地使用！
