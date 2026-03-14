# relative-position

> 告别那些繁琐的坐标计算！用 Python 轻松找到桌面应用中元素的准确位置 🎯

## ✨ 特性

`relative-position` 是一个让窗口元素定位变得简单有趣的跨平台 Python 库。它就像给你的鼠标装上了 GPS 导航系统：

- 🎯 **精准定位**：告别手动计算像素，让代码帮你找到元素
- 🌍 **跨平台支持**：Linux (X11/Wayland) 和 Windows 全覆盖，一个库走天下
- 🎮 **游戏化配置**：用代码定义 UI 元素，像玩游戏一样简单
- 🔧 **智能参考点**：支持 9 种参考点方向，满足各种布局需求
- 🤖 **自动适配**：智能识别当前平台，加载最优实现

## 🚀 快速开始

### 安装

```bash
pip install relative-position
```

> 或者从源码安装（适合喜欢折腾的开发者）：

```bash
git clone https://github.com/mikigo/relative-position.git
cd relative-position
pip install -e .
```

## 📚 使用指南

### 窥探窗口信息

想知道当前电脑上都有哪些窗口？一秒钟搞定：

```python
from relative_position import get_window_info_provider

# 自动识别平台，获取对应的窗口信息提供者
provider = get_window_info_provider()

# 获取所有窗口信息（这比侦探调查还快）
windows = provider.window_info()
for name, info in windows.items():
    print(f"发现目标: {name}")
    print(f"📍 位置: {info['location']}")
```

### 使用 Ele 类定义元素（推荐）

告别古老的 INI 文件，用代码定义元素，就像写诗一样优雅：

```python
from relative_position import Ele, Elements, get_button_center

# 定义一个元素（就像定义你的好朋友）
close_button = Ele(
    direction="left_bottom",  # 参考点方向
    location=[20, 20, 50, 35]  # x, y, width, height
)

# 或者一次定义多个元素（就像组建一个梦之队）
elements = Elements()
elements.add("close_button", close_button)
elements.add("open_button", Ele(direction="right_top", location=[10, 10, 40, 30]))
elements.add("menu_item", Ele(direction="left_top", location=[100, 200, 80, 40]))

# 使用元素集合
btn_center = get_button_center(
    app_name="notepad.exe",  # Windows 用户
    # app_name="gedit",      # Linux 用户
    config_path=elements      # 直接传入 Elements 对象
)

# 获取元素坐标（比找宝藏还准）
x, y = btn_center.btn_center("close_button")
print(f"🎯 close_button 瞄准点: ({x}, {y})")

# 获取窗口信息
window_x, window_y = btn_center.window_left_top_position()
width, height = btn_center.window_sizes()
print(f"📐 窗口位置: ({window_x}, {window_y})")
print(f"📏 窗口大小: {width} x {height}")
```

### 支持的配置方式

我们支持多种配置方式，总有一款适合你：

- ✅ **Ele 对象**：单个元素定义（最灵活）
- ✅ **Elements 对象**：元素集合管理（推荐）
- ✅ **字典配置**：数据驱动（适合配置管理系统）
- ❌ **INI 文件**：已不再支持（拥抱代码定义吧！）

## 🎨 参考点方向 (direction)

就像选择最佳的观察角度一样，我们提供了 9 种参考点方向：

| 方向 | 说明 | 适用场景 |
|------|------|----------|
| `left_top` | 左上角 | 传统的左上定位 |
| `right_top` | 右上角 | 适合右上角按钮 |
| `left_bottom` | 左下角 | 底部左侧元素 |
| `right_bottom` | 右下角 | 底部右侧元素 |
| `top_center` | 上边界中心 | 顶部中间按钮 |
| `bottom_center` | 下边界中心 | 底部中间按钮 |
| `left_center` | 左边界中心 | 左侧中间元素 |
| `right_center` | 右边界中心 | 右侧中间元素 |
| `window_size` | 整个窗口 | 窗口级别操作 |

## 🏗️ API 参考

### Ele 类

元素定义的核心类，让你的 UI 元素定义变得有型：

```python
close_button = Ele(
    direction="left_bottom",
    location=[20, 20, 50, 35]
)
```

#### 属性
- `direction`: 参考点方向
- `location`: 坐标列表 [x, y, width, height]
- `x`, `y`, `width`, `height`: 便捷属性访问器

### Elements 类

元素集合管理器，让你像管理团队一样管理多个元素：

```python
elements = Elements()
elements.add("close_button", Ele(...))
elements.add("open_button", Ele(...))

# 像字典一样访问
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

### ButtonCenter 类

元素定位的主力军，提供丰富的窗口和元素操作方法：

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

## 🖥️ 平台实现细节

### Linux 平台

我们的 Linux 实现就像一个多面手，能够适应不同的环境：

#### X11 实现
- **工具链**: `xdotool` + `xwininfo`
- **特点**: 稳定可靠，经过长期验证
- **适用场景**: 传统桌面环境（GNOME、KDE）

#### Wayland 实现
- **工具链**: `dtkwmjack` 库
- **特点**: 现代化设计，支持最新桌面
- **适用场景**: Deepin 等使用 Wayland 的发行版

### Windows 平台

Windows 实现就像一个熟练的 Windows 专家：

- **工具链**: Windows API (user32.dll)
- **特点**: 原生性能，集成度高
- **依赖**: `psutil` 库（用于进程管理）
- **额外功能**: 支持快捷键操作（ESC 等）

## 🏛️ 架构设计

我们的架构就像一个精心设计的迷宫，简单却充满智慧：

```
relative_position/
├── elements.py              # Ele 和 Elements 类（元素定义核心）
├── config.py               # 平台检测和配置（自动识别）
├── exceptions.py            # 自定义异常（友好的错误提示）
├── utils.py                # 工具函数（日志、命令、快捷键）
├── __init__.py             # 模块入口（统一的 API）
├── linux/                  # Linux 平台实现
│   ├── base.py            # 抽象基类（接口定义）
│   ├── main.py            # ButtonCenter 实现
│   ├── x11_wininfo.py    # X11 窗口信息提供者
│   └── wayland_wininfo.py # Wayland 窗口信息提供者
└── windows/                # Windows 平台实现
    ├── main.py            # ButtonCenter 实现
    └── windows_wininfo.py # Windows 窗口信息提供者
```

### 设计优势 🎯

- **解耦**: X11 和 Wayland 实现完全独立，互不干扰
- **可扩展**: 想要支持新的显示服务器？实现一个类就行
- **易维护**: 统一的接口定义，代码结构像艺术品一样清晰
- **平台优化**: 每个平台都可以独立优化，不相互影响

## 📦 依赖管理

### 所有平台
- Python 3.6+

### Windows 平台
```bash
pip install psutil>=5.9.0
```

### Linux 平台
```bash
# 基础依赖
pip install dbus-python>=1.3.2

# X11 依赖（如果使用 X11）
sudo apt-get install xdotool x11-utils  # Debian/Ubuntu
sudo yum install xdotool xorg-xwininfo  # RHEL/CentOS

# Wayland 依赖（如果使用 Wayland）
# 需要安装 dtkwmjack 库（Deepin 特定）
```

## 🎓 示例代码

更多示例请查看项目中的示例文件：

- `example_ele.py`: Ele 类使用示例
- `example.py`: 基础使用示例

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
