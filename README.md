# relative-position

> 告别那些繁琐的坐标计算！用 Python 轻松找到桌面应用中元素的准确位置 🎯

## ✨ 特性

`relative-position` 是一个让窗口元素定位变得简单有趣的跨平台 Python 库。它就像给你的鼠标装上了 GPS 导航系统：

- 🎯 **精准定位**：告别手动计算像素，让代码帮你找到元素
- 🌍 **跨平台支持**：Linux (X11/Wayland) 和 Windows 全覆盖，一个库走天下
- 🎮 **代码定义**：用 Python 类定义 UI 元素，类型安全，IDE 友好
- 🔧 **智能参考点**：支持 9 种参考点方向，满足各种布局需求
- 🚀 **自动适配**：智能识别当前平台，加载最优实现
- 🤖 **统一接口**：使用 pyautogui 进行跨平台鼠标操作

## 🚀 快速开始

### 安装

```bash
pip install relative-position
```

或者从源码安装：

```bash
git clone https://github.com/mikigo/relative-position.git
cd relative-position
pip install -e .
```

## 📚 使用指南

### 最简洁的使用方式（推荐）⭐

```python
from relative_position import App

# 创建应用实例
app = App(appname="explorer.exe")  # Windows
# app = App(appname="gedit")       # Linux

# 使用 app.Ele() 创建元素（自动关联到应用）
new_file_btn = app.Ele(
    direction="left_top",      # 或使用 Direction.LEFT_TOP 枚举
    location=[20, 20, 50, 35]  # [x, y, width, height]
)

# 操作元素
new_file_btn.click()        # 点击
new_file_btn.right_click()  # 右键点击
new_file_btn.double_click() # 双击

# 获取元素中心坐标
x, y = new_file_btn.center()
print(f"🎯 元素中心坐标: ({x}, {y})")

# 窗口操作
app.focus_window()         # 聚焦窗口
wx, wy = app.window_position()
width, height = app.window_size()
print(f"📐 窗口位置: ({wx}, {wy}), 大小: {width} x {height}")
```

### 使用 Direction 枚举（类型安全）

```python
from relative_position import App, Direction

app = App(appname="explorer.exe")

# 使用枚举定义元素（推荐）
close_btn = app.Ele(
    direction=Direction.LEFT_BOTTOM,
    location=[20, 20, 50, 35]
)

# 枚举提供完整的类型检查和 IDE 自动补全
close_btn.click()
```

### 使用 Elements 管理多个元素

```python
from relative_position import Ele, Elements, Direction

# 创建元素集合
elements = Elements()
elements.add("close_button", Ele(direction=Direction.LEFT_BOTTOM, location=[20, 20, 50, 35]))
elements.add("open_button", Ele(direction=Direction.RIGHT_TOP, location=[10, 10, 40, 30]))

# 像字典一样访问
close_btn = elements["close_button"]
print(f"方向: {close_btn.direction}, 位置: {close_btn.location}")
```

## 🎨 参考点方向 (Direction)

`Direction` 枚举提供了 9 种参考点方向：

| 枚举值 | 字符串值 | 说明 | 适用场景 |
|--------|----------|------|----------|
| `Direction.LEFT_TOP` | `"left_top"` | 左上角 | 传统的左上定位 |
| `Direction.RIGHT_TOP` | `"right_top"` | 右上角 | 适合右上角按钮 |
| `Direction.LEFT_BOTTOM` | `"left_bottom"` | 左下角 | 底部左侧元素 |
| `Direction.RIGHT_BOTTOM` | `"right_bottom"` | 右下角 | 底部右侧元素 |
| `Direction.TOP_CENTER` | `"top_center"` | 上边界中心 | 顶部中间按钮 |
| `Direction.BOTTOM_CENTER` | `"bottom_center"` | 下边界中心 | 底部中间按钮 |
| `Direction.LEFT_CENTER` | `"left_center"` | 左边界中心 | 左侧中间元素 |
| `Direction.RIGHT_CENTER` | `"right_center"` | 右边界中心 | 右侧中间元素 |
| `Direction.WINDOW_SIZE` | `"window_size"` | 整个窗口 | 窗口级别操作 |

## 🏗️ API 参考

### Ele 类

元素定义的核心类，支持枚举和字符串两种方式：

```python
from relative_position import Ele, Direction

# 使用枚举（推荐）
btn = Ele(direction=Direction.LEFT_TOP, location=[20, 20, 50, 35])

# 使用字符串（向后兼容）
btn = Ele(direction="left_top", location=[20, 20, 50, 35])
```

#### 属性
- `direction`: 参考点方向（Direction 枚举）
- `location`: 坐标列表 `[x, y, width, height]`
- `x`, `y`, `width`, `height`: 便捷属性访问器

#### 方法（关联到 App 后可用）
- `center()`: 获取元素中心坐标
- `click()`: 点击元素
- `right_click()`: 右键点击元素
- `double_click()`: 双击元素
- `hover()`: 鼠标悬停在元素上

#### 其他方法
- `get_position()`: 获取位置信息 `(direction, location)`
- `to_dict()`: 转换为字典
- `set_app(app, name=None)`: 关联元素到 App 实例

### Elements 类

元素集合管理器：

```python
elements = Elements()
elements.add("close_button", Ele(...))
elements.add("open_button", Ele(...))

# 访问元素
element = elements["close_button"]

# 遍历所有元素
for name in elements:
    print(f"{name}: {elements[name]}")
```

#### 方法
- `add(name, ele)`: 添加元素
- `get(name)`: 获取元素
- `remove(name)`: 移除元素
- `list_names()`: 获取所有元素名称
- `to_dict()`: 转换为字典

### App 类（简洁 API）⭐

提供最简洁的应用程序 UI 元素操作接口：

```python
from relative_position import App

app = App(appname="explorer.exe")
btn = app.Ele(direction=Direction.LEFT_TOP, location=[20, 20, 50, 35])
```

#### 构造函数参数
- `appname`: 应用程序名称
  - Windows: `"explorer.exe"`, `"notepad.exe"` 等
  - Linux: `"gedit"`, `"firefox"` 等
- `number`: 窗口索引，默认 `-1`（最后一个窗口）
- `pause`: 每个操作步骤之前暂停的时间（秒）
- `retry`: 重试次数

#### 方法
- `Ele(direction, location, name=None)`: 创建并注册元素
- `get_center(element)`: 获取元素中心坐标（支持 Ele 对象或元素名称）
- `focus_window()`: 将应用窗口置顶并聚焦
- `window_info()`: 获取窗口信息
- `window_size()`: 获取窗口大小
- `window_center()`: 获取窗口中心坐标
- `window_position()`: 获取窗口左上角坐标

### RelativePosition 类

底层实现类，提供完整的窗口和元素操作方法（通常通过 App 类间接使用）。

#### 窗口定位方法
- `window_left_top_position()`: 获取窗口左上角坐标
- `window_right_top_position()`: 获取窗口右上角坐标
- `window_left_bottom_position()`: 获取窗口左下角坐标
- `window_right_bottom_position()`: 获取窗口右下角坐标
- `window_center()`: 获取窗口中心坐标
- `window_sizes()`: 获取窗口大小
- `window_location_and_sizes()`: 获取窗口位置和大小

#### 元素定位方法
- `btn_center(btn_name, ...)`: 获取指定按钮的中心坐标
- `btn_size(btn_name, ...)`: 获取指定按钮的大小和位置
- `btn_info(btn_name)`: 获取元素的相对位置和参考系

#### 窗口管理方法
- `get_windows_number(name)`: 获取应用窗口数量
- `get_windows_id(name)`: 获取窗口 ID 列表
- `focus_windows(app_name)`: 聚焦指定窗口
- `get_lastest_window_id(app_name)`: 获取最新窗口 ID

### Mouse 类

跨平台鼠标操作工具类：

```python
from relative_position import Mouse

Mouse.move_to(500, 500)        # 移动鼠标
Mouse.click(button='left')       # 左键点击
Mouse.click(button='right')      # 右键点击
Mouse.double_click(button='left') # 双击
```

## 🖥️ 平台实现细节

### Linux 平台

#### X11 实现
- **工具链**: `xdotool` + `xwininfo`
- **特点**: 稳定可靠，经过长期验证
- **适用场景**: 传统桌面环境（GNOME、KDE）

#### Wayland 实现
- **工具链**: `dtkwmjack` 库
- **特点**: 现代化设计，支持最新桌面
- **适用场景**: Deepin 等使用 Wayland 的发行版

### Windows 平台
- **工具链**: Windows API (user32.dll)
- **特点**: 原生性能，集成度高
- **鼠标操作**: pyautogui（跨平台统一接口）

## 🏛️ 架构设计

```
relative_position/
├── __init__.py             # 模块入口（导出 Ele, Direction, App, Mouse）
├── elements.py             # Ele, Elements, Direction 类
├── app.py                 # App, Mouse 类（用户 API）
├── config.py              # 平台检测和配置
├── exceptions.py           # 自定义异常
├── utils.py              # 工具函数（日志、命令、快捷键）
├── linux/                # Linux 平台实现
│   ├── base.py          # RelativePositionBase 抽象基类
│   ├── main.py          # RelativePosition 实现
│   ├── x11_wininfo.py  # X11 窗口信息提供者
│   └── wayland_wininfo.py # Wayland 窗口信息提供者
└── windows/              # Windows 平台实现
    ├── main.py          # RelativePosition 实现
    └── windows_wininfo.py # Windows 窗口信息提供者
```

### 设计优势
- **解耦**: X11 和 Wayland 实现完全独立，互不干扰
- **可扩展**: 想要支持新的显示服务器？实现一个类就行
- **易维护**: 统一的接口定义，代码结构清晰
- **类型安全**: 使用枚举提供编译时类型检查
- **平台优化**: 每个平台都可以独立优化，不相互影响

## 📦 依赖管理

### 所有平台
- Python 3.6+

### 核心依赖（自动安装）
- `pyautogui>=0.9.54` - 跨平台鼠标操作
- `psutil>=5.9.0` - Windows 进程管理
- `dbus-python>=1.3.2` - Linux D-Bus 支持

### Linux 平台额外依赖

#### X11 环境
```bash
sudo apt-get install xdotool x11-utils  # Debian/Ubuntu
sudo yum install xdotool xorg-xwininfo  # RHEL/CentOS
```

#### Wayland 环境
需要安装 dtkwmjack 库（Deepin 特定）

## 🎓 示例代码

更多示例请查看项目中的示例文件：

- `example_simple_api.py`: 简洁 API 使用示例（推荐）⭐
- `example_ele.py`: Ele 类使用示例

## 🤝 贡献指南

欢迎贡献！不管是修复 bug 还是添加新功能，我们都感激不尽：

1. Fork 本项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交一个 Pull Request

## 📄 许可证

本项目采用 Apache 2.0 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

> **提示**: 如果你在使用过程中遇到问题，不要犹豫，提交一个 issue。我们通常会在 24 小时内响应（除非我们在睡觉 😴）

**让窗口定位变得简单有趣，从 `relative-position` 开始！** 🚀
