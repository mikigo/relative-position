#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
示例脚本：演示如何使用 relative-position 库
"""

import sys
import io

# 设置 stdout 编码为 UTF-8
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from relative_position import (
    get_button_center,
    get_window_info_provider,
    config,
    IS_WINDOWS,
    IS_X11,
    IS_WAYLAND,
)


def example_window_info():
    """示例：获取窗口信息"""
    print("=== 获取窗口信息示例 ===")
    print(f"当前平台: Windows={IS_WINDOWS}, X11={IS_X11}, Wayland={IS_WAYLAND}\n")

    # 获取窗口信息提供者（自动检测平台）
    provider = get_window_info_provider()
    provider_type = type(provider).__name__
    print(f"使用窗口信息提供者: {provider_type}\n")

    windows = provider.window_info()

    print(f"找到 {len(windows)} 个应用:")
    for i, (name, info) in enumerate(windows.items(), 1):
        print(f"\n{i}. {name}")
        if isinstance(info, dict):
            loc = info.get('location', (0, 0, 0, 0))
            title = info.get('title', '')
            pid = info.get('pid', '')
            print(f"   位置: {loc}")
            if title:
                print(f"   标题: {title}")
            if pid:
                print(f"   PID: {pid}")
        elif isinstance(info, list):
            for j, win in enumerate(info, 1):
                loc = win.get('location', (0, 0, 0, 0))
                title = win.get('title', '')
                pid = win.get('pid', '')
                print(f"   窗口 {j}: 位置 {loc}")
                if title:
                    print(f"         标题: {title}")
                if pid:
                    print(f"         PID: {pid}")


def example_button_center():
    """示例：使用配置文件获取按钮坐标"""
    print("\n=== 使用配置文件获取按钮坐标示例 ===")

    # 根据平台选择应用名称
    if IS_WINDOWS:
        # Windows 示例 - 需要先启动 notepad
        app_name = "notepad.exe"
    elif IS_X11:
        # Linux X11 示例 - 需要先启动相应应用
        app_name = "gedit"
    else:  # IS_WAYLAND
        # Linux Wayland 示例
        app_name = "dde-file-manager"

    print(f"应用名称: {app_name}")
    print(f"显示服务器: {'Windows' if IS_WINDOWS else 'X11' if IS_X11 else 'Wayland'}")
    print("注意: 请确保应用已经启动\n")

    try:
        # 创建 ButtonCenter 实例（自动检测平台）
        btn_center = get_button_center(
            app_name=app_name,
            config_path="example_config.ini"
        )

        # 获取窗口信息
        print("窗口信息:")
        x, y = btn_center.window_left_top_position()
        width, height = btn_center.window_sizes()
        print(f"  左上角: ({x}, {y})")
        print(f"  大小: {width} x {height}")

        # 获取窗口数量
        count = btn_center.get_windows_number(app_name)
        print(f"  窗口数量: {count}")

        # 获取按钮信息
        print("\n配置的按钮:")
        from configparser import ConfigParser
        conf = ConfigParser()
        conf.read("example_config.ini")
        for section in conf.sections():
            print(f"  - {section}")

    except Exception as e:
        print(f"错误: {e}")
        print("提示: 请确保应用已启动")


def main():
    """主函数"""
    print("relative-position 库使用示例\n")

    # 显示窗口信息
    example_window_info()

    # 显示按钮定位示例
    example_button_center()

    print("\n示例完成！")


if __name__ == "__main__":
    main()
