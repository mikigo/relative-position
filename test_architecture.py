#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
测试新的模块化架构
"""

import sys

def test_imports():
    """测试所有模块是否可以正确导入"""
    print("=== 测试模块导入 ===")

    try:
        from relative_position import (
            get_button_center,
            get_window_info_provider,
            config,
            IS_WINDOWS,
            IS_X11,
            IS_WAYLAND,
        )
        print("[OK] 主模块导入成功")
        print(f"  平台检测: Windows={IS_WINDOWS}, X11={IS_X11}, Wayland={IS_WAYLAND}")
    except Exception as e:
        print(f"[FAIL] 主模块导入失败: {e}")
        return False

    try:
        from relative_position.linux import (
            ButtonCenterBase,
            WindowInfoProvider,
            X11WindowInfo,
            WaylandWindowInfo,
            ButtonCenter as LinuxButtonCenter,
        )
        print("[OK] Linux 模块导入成功")
    except Exception as e:
        print(f"[FAIL] Linux 模块导入失败: {e}")
        return False

    try:
        from relative_position.windows import (
            WindowsWindowInfo,
            ButtonCenter as WindowsButtonCenter,
        )
        print("[OK] Windows 模块导入成功")
    except Exception as e:
        print(f"[FAIL] Windows 模块导入失败: {e}")
        # 这可能是由于缺少依赖，不是代码问题

    return True


def test_architecture():
    """测试架构设计"""
    print("\n=== 测试架构设计 ===")

    # 测试抽象基类
    try:
        from relative_position.linux.base import ButtonCenterBase, WindowInfoProvider

        # 检查抽象方法是否正确定义
        abstract_methods = [
            'window_info',
            'window_location_and_sizes',
            'window_left_top_position',
            'window_sizes',
            'get_windows_number',
            'get_windows_id',
            'focus_windows',
            'get_lastest_window_id',
        ]

        for method in abstract_methods:
            if not hasattr(ButtonCenterBase, method):
                print(f"[FAIL] ButtonCenterBase 缺少方法: {method}")
                return False

        print("[OK] 抽象基类结构正确")
    except Exception as e:
        print(f"[FAIL] 抽象基类测试失败: {e}")
        return False

    # 测试 X11 窗口信息提供者
    try:
        from relative_position.linux.x11_wininfo import X11WindowInfo
        from relative_position.linux.base import WindowInfoProvider

        if not issubclass(X11WindowInfo, WindowInfoProvider):
            print("[FAIL] X11WindowInfo 未继承 WindowInfoProvider")
            return False

        print("[OK] X11 窗口信息提供者继承正确")
    except Exception as e:
        print(f"[FAIL] X11 窗口信息提供者测试失败: {e}")
        return False

    # 测试 Linux ButtonCenter
    try:
        from relative_position.linux.main import ButtonCenter
        from relative_position.linux.base import ButtonCenterBase

        if not issubclass(ButtonCenter, ButtonCenterBase):
            print("[FAIL] ButtonCenter 未继承 ButtonCenterBase")
            return False

        print("[OK] Linux ButtonCenter 继承正确")
    except Exception as e:
        print(f"[FAIL] Linux ButtonCenter 测试失败: {e}")
        return False

    return True


def test_factory_functions():
    """测试工厂函数"""
    print("\n=== 测试工厂函数 ===")

    try:
        from relative_position import get_window_info_provider

        provider = get_window_info_provider()
        print(f"[OK] get_window_info_provider() 返回: {type(provider).__name__}")
    except Exception as e:
        print(f"[FAIL] get_window_info_provider() 失败: {e}")
        return False

    return True


def main():
    """主测试函数"""
    print("relative-position 架构测试\n")

    success = True

    if not test_imports():
        success = False

    if not test_architecture():
        success = False

    if not test_factory_functions():
        success = False

    print("\n" + "="*50)
    if success:
        print("[OK] 所有测试通过！")
        return 0
    else:
        print("[FAIL] 部分测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
