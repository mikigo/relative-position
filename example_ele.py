#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
示例脚本：演示如何使用 Ele 类定义元素
"""

import sys
import io

# 设置 stdout 编码为 UTF-8
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from relative_position import Ele, Elements, Direction, App


def example_single_element():
    """示例：创建单个元素"""
    print("=== 创建单个元素示例 ===")

    # 使用 Direction 枚举定义元素
    close_button = Ele(
        direction=Direction.LEFT_BOTTOM,
        location=[20, 20, 50, 35]
    )

    print(f"元素名称: close_button")
    print(f"方向: {close_button.direction}")
    print(f"位置: {close_button.location}")
    print(f"坐标: x={close_button.x}, y={close_button.y}")
    print(f"大小: width={close_button.width}, height={close_button.height}")


def example_elements_collection():
    """示例：创建元素集合"""
    print("\n=== 创建元素集合示例 ===")

    # 创建元素集合
    elements = Elements()

    # 添加多个元素（使用枚举）
    elements.add("close_button", Ele(
        direction=Direction.LEFT_BOTTOM,
        location=[20, 20, 50, 35]
    ))

    elements.add("open_button", Ele(
        direction=Direction.RIGHT_TOP,
        location=[10, 10, 40, 30]
    ))

    elements.add("menu_item", Ele(
        direction=Direction.LEFT_TOP,
        location=[100, 200, 80, 40]
    ))

    print(f"元素数量: {len(elements)}")
    print(f"元素列表: {elements.list_names()}")

    # 访问元素
    for element_name in elements:
        ele = elements[element_name]
        print(f"\n{element_name}:")
        print(f"  方向: {ele.direction}")
        print(f"  位置: {ele.location}")


def example_with_app():
    """示例：使用 Ele 对象与 App 结合"""
    print("\n=== 与 App 结合使用示例 ===")

    # 创建元素集合
    elements = Elements({
        "close_button": Ele(direction=Direction.LEFT_BOTTOM, location=[20, 20, 50, 35]),
        "open_button": Ele(direction=Direction.RIGHT_TOP, location=[10, 10, 40, 30]),
    })

    # 注意：此功能需要应用正在运行
    print("注意：以下示例需要应用正在运行")
    print("示例代码：")

    example_code = """
from relative_position import Ele, Elements, Direction, App

# 创建应用实例
app = App(appname="notepad.exe")  # Windows
# app = App(appname="gedit")       # Linux

# 创建元素集合
elements = Elements()
elements.add("close_button", Ele(direction=Direction.LEFT_BOTTOM, location=[20, 20, 50, 35]))

# 将元素集合添加到应用
app._button_center._elements_dict = elements.to_dict()

# 获取按钮中心坐标
x, y = app.get_center("close_button")
print(f"close_button 中心坐标: ({x}, {y})")

# 或者直接使用 app.Ele() 创建元素（推荐）
btn = app.Ele(direction=Direction.LEFT_TOP, location=[100, 100, 50, 30], name="my_button")
btn.click()
"""

    print(example_code)


def example_valid_directions():
    """示例：有效的方向"""
    print("\n=== 有效方向示例 ===")

    print("支持的方向:")
    for direction in Direction:
        print(f"  - {direction.name}: {direction.value}")


def example_error_handling():
    """示例：错误处理"""
    print("\n=== 错误处理示例 ===")

    try:
        # 无效的方向（字符串）
        invalid_ele = Ele(
            direction="invalid_direction",
            location=[10, 10, 40, 30]
        )
    except ValueError as e:
        print(f"捕获到错误: {e}")

    try:
        # 无效的 location 格式
        invalid_ele = Ele(
            direction=Direction.LEFT_TOP,
            location=[10, 10, 40]
        )
    except ValueError as e:
        print(f"捕获到错误: {e}")


def main():
    """主函数"""
    print("relative-position Ele 类使用示例\n")

    example_single_element()
    example_elements_collection()
    example_with_app()
    example_valid_directions()
    example_error_handling()

    print("\n示例完成！")


if __name__ == "__main__":
    main()
