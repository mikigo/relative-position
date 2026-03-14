# relative-position

相对元素定位 - 获取桌面应用中元素在屏幕中的坐标

## 功能

这个项目提供了一个跨平台的Python库，用于获取桌面应用程序中元素的相对坐标。支持：
- 获取窗口的位置和大小
- 根据配置文件计算控件元素的屏幕坐标
- 支持多种参考点（左上角、右上角、左下角、右下角、边界中心等）
- 自动根据平台加载相应的实现（Linux X11/Wayland 和 Windows）

## 支持的平台

- Linux (X11 和 Wayland)
- Windows

## 安装

```bash
pip install -r requirements.txt
```

## 使用示例

### 获取窗口信息

```python
from relative_position import get_window_info_provider

# 获取窗口信息提供者
provider = get_window_info_provider()

# 获取所有窗口信息
windows = provider.window_info()
for name, info in windows.items():
    print(f"应用: {name}")
    print(f"位置: {info['location']}")
```

### 使用配置文件定位元素

首先创建一个配置文件（如 `example_config.ini`）：

```ini
[close_button]
direction = right_top
location = 10, 10, 40, 30

[open_button]
direction = left_bottom
location = 20, 20, 50, 35
```

然后使用以下代码获取元素坐标：

```python
from relative_position import get_button_center

# 创建 ButtonCenter 实例
btn_center = get_button_center(
    app_name="notepad.exe",  # Windows
    # app_name="gedit",      # Linux
    config_path="example_config.ini"
)

# 获取按钮中心坐标
x, y = btn_center.btn_center("close_button")
print(f"close_button 中心坐标: ({x}, {y})")

# 获取窗口信息
window_x, window_y = btn_center.window_left_top_position()
width, height = btn_center.window_sizes()
print(f"窗口位置: ({window_x}, {window_y})")
print(f"窗口大小: {width} x {height}")
```

## 配置文件格式

配置文件使用 INI 格式，每个控件定义一个节：

```ini
[控件名称]
direction = 参考点方向
location = x, y, width, height
```

### 参考点方向 (direction)

- `left_top`: 相对于窗口左上角
- `right_top`: 相对于窗口右上角
- `left_bottom`: 相对于窗口左下角
- `right_bottom`: 相对于窗口右下角
- `top_center`: 相对于窗口上边界中心
- `bottom_center`: 相对于窗口下边界中心
- `left_center`: 相对于窗口左边界中心
- `right_center`: 相对于窗口右边界中心
- `window_size`: 使用整个窗口

## API 参考

### ButtonCenter

主要类，用于计算控件元素的屏幕坐标。

#### 方法

- `window_left_top_position()`: 获取窗口左上角坐标
- `window_right_top_position()`: 获取窗口右上角坐标
- `window_left_bottom_position()`: 获取窗口左下角坐标
- `window_right_bottom_position()`: 获取窗口右下角坐标
- `window_center()`: 获取窗口中心坐标
- `window_sizes()`: 获取窗口大小
- `window_location_and_sizes()`: 获取窗口位置和大小
- `btn_center(btn_name, ...)`: 获取指定按钮的中心坐标
- `btn_size(btn_name, ...)`: 获取指定按钮的大小和位置
- `get_windows_number(name)`: 获取应用窗口数量
- `focus_windows(app_name)`: 聚焦窗口

### 平台差异

#### Linux

- **X11**: 使用 `xdotool` 和 `xwininfo` 命令，通过 `X11WindowInfo` 类实现
- **Wayland**: 使用 `dtkwmjack` 库（需要安装），通过 `WaylandWindowInfo` 类实现
- 两种实现都继承自 `ButtonCenterBase` 抽象基类，提供统一的接口

#### Windows

- 使用 Windows API (user32.dll)，通过 `WindowsWindowInfo` 类实现
- 需要安装 `psutil` 库
- 支持快捷键操作（ESC 等）

## 架构

### 模块化设计

项目采用模块化设计，通过抽象基类定义统一接口：

```
relative_position/
├── base.py              # 抽象基类（ButtonCenterBase, WindowInfoProvider）
├── linux/
│   ├── main.py          # Linux ButtonCenter 实现
│   ├── x11_wininfo.py   # X11 窗口信息提供者
│   └── wayland_wininfo.py # Wayland 窗口信息提供者
└── windows/
    ├── main.py          # Windows ButtonCenter 实现
    └── windows_wininfo.py # Windows 窗口信息提供者
```

### 优势

- **解耦**: X11 和 Wayland 实现完全独立，互不影响
- **可扩展**: 添加新的显示服务器支持只需实现新的窗口信息提供者
- **易维护**: 统一的接口定义，代码结构清晰
- **平台优化**: 每个平台可以独立优化，不影响其他平台

## 依赖

### 所有平台
- Python 3.6+

### Windows
- psutil>=5.9.0

### Linux
- dbus-python>=1.3.2
- xdotool (X11)
- x11-utils (X11)

## 许可证

请查看 LICENSE 文件了解详细信息。
