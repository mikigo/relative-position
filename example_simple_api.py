#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
示例脚本：演示如何使用新的简洁 API
"""

import sys
import io

# 设置 stdout 编码为 UTF-8
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from relative_position import App, Ele, Mouse


def example_simple_usage():
    """示例：最简洁的 API 使用方式（推荐）⭐"""
    print("=== 最简洁 API 使用示例（推荐）⭐ ===\n")

    # 创建应用实例
    app = App(appname="explorer.exe")

    print("1. 使用 app.Ele() 创建元素（最简洁）：")
    # 定义元素（一步创建并关联到应用）
    new_file_btn = app.Ele(
        direction="left_top",
        location=[20, 20, 50, 35]
    )

    print("   元素已创建并自动关联到 app")

    print("\n2. 获取元素中心坐标：")
    # 获取元素中心坐标
    try:
        x, y = new_file_btn.center()
        print(f"   new_file_btn 中心坐标: ({x}, {y})")
    except Exception as e:
        print(f"   注意: 需要应用正在运行。错误: {e}")

    print("\n3. 鼠标操作示例（需要应用正在运行）：")
    # 点击元素
    print("   new_file_btn.click()")
    # new_file_btn.click()  # 取消注释以实际执行

    # 右键点击元素
    print("   new_file_btn.right_click()")
    # new_file_btn.right_click()  # 取消注释以实际执行

    # 双击元素
    print("   new_file_btn.double_click()")
    # new_file_btn.double_click()  # 取消注释以实际执行

    print("\n4. 鼠标悬停：")
    print("   new_file_btn.hover()")
    # new_file_btn.hover()  # 取消注释以实际执行


def example_with_app_association():
    """示例：在创建元素时直接关联 App"""
    print("\n\n=== 创建元素时直接关联 App 示例 ===\n")

    # 创建应用实例
    app = App(appname="notepad.exe")

    print("1. 创建元素时关联 App：")
    # 方式二：在创建时直接关联 App
    save_btn = Ele(
        direction="right_bottom",
        location=[100, 50, 60, 30],
        app=app,
        name="save_button"
    )

    print("   save_btn 元素已关联到 app")

    print("\n2. 多个元素操作：")
    # 定义多个元素
    close_btn = Ele(
        direction="right_top",
        location=[30, 20, 50, 35],
        app=app
    )
    print("   close_btn 元素已自动注册")

    # 获取窗口信息
    print("\n3. 窗口操作：")
    try:
        app.focus_window()
        print("   窗口已置顶并聚焦")

        wx, wy = app.window_position()
        print(f"   窗口左上角坐标: ({wx}, {wy})")

        width, height = app.window_size()
        print(f"   窗口大小: {width}x{height}")

        cx, cy = app.window_center()
        print(f"   窗口中心坐标: ({cx}, {cy})")
    except Exception as e:
        print(f"   注意: 需要应用正在运行。错误: {e}")


def example_mouse_operations():
    """示例：鼠标操作类"""
    print("\n\n=== 鼠标操作类示例 ===\n")

    print("1. 鼠标移动：")
    print("   Mouse.move_to(500, 500)")
    # Mouse.move_to(500, 500)  # 取消注释以实际执行

    print("\n2. 鼠标点击：")
    print("   Mouse.click(button='left', clicks=1)")
    # Mouse.click(button='left', clicks=1)  # 取消注释以实际执行

    print("\n3. 鼠标右键点击：")
    print("   Mouse.click(button='right', clicks=1)")
    # Mouse.click(button='right', clicks=1)  # 取消注释以实际执行

    print("\n4. 鼠标双击：")
    print("   Mouse.double_click(button='left')")
    # Mouse.double_click(button='left')  # 取消注释以实际执行

    print("\n5. 元素悬停：")
    print("   element.hover()")
    # element.hover()  # 取消注释以实际执行


def example_combined_usage():
    """示例：综合使用示例"""
    print("\n\n=== 综合使用示例 ===\n")

    print("方式一：使用 app.Ele() 方法（推荐）⭐")
    example_code1 = '''
from relative_position import App

# 创建应用实例
app = App(appname="explorer.exe")

# 使用 app.Ele() 创建元素（一步完成）
new_folder_btn = app.Ele(
    direction="left_top",
    location=[20, 80, 50, 35]
)

# 定义其他元素
file_menu = app.Ele(
    direction="top_center",
    location=[-150, 0, 60, 30]
)

# 执行自动化操作
app.focus_window()  # 聚焦窗口
file_menu.click()   # 点击文件菜单
new_folder_btn.click()  # 点击新建文件夹按钮

# 或者使用右键菜单
new_folder_btn.right_click()  # 右键点击
'''

    print(example_code1)

    print("\n方式二：使用 Ele() 构造函数并关联到 App")
    example_code2 = '''
from relative_position import App, Ele

# 创建应用实例
app = App(appname="explorer.exe")

# 使用 Ele() 构造函数
new_folder_btn = Ele(
    direction="left_top",
    location=[20, 80, 50, 35]
)

# 关联元素到应用
new_folder_btn.set_app(app, name="new_folder")

# 或者直接在创建时关联
file_menu = Ele(
    direction="top_center",
    location=[-150, 0, 60, 30],
    app=app
)

# 执行自动化操作
app.focus_window()
file_menu.click()
new_folder_btn.click()
'''

    print(example_code2)


def main():
    """主函数"""
    print("relative-position 最简洁 API 使用示例\n")
    print("=" * 50)

    example_simple_usage()
    example_with_app_association()
    example_mouse_operations()
    example_combined_usage()

    print("\n" + "=" * 50)
    print("\n示例完成！")
    print("\n推荐使用方式：")
    print("- 使用 app.Ele() 方法创建元素（最简洁）⭐")
    print("- 元素创建后直接可以调用 click(), right_click() 等方法")
    print("\n注意：")
    print("- 实际执行鼠标操作时，请确保目标应用正在运行")
    print("- 取消注释相关代码以执行实际的鼠标操作")
    print("- 不同平台（Windows/Linux）可能有不同的表现")


if __name__ == "__main__":
    main()
