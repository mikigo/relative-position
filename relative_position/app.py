#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
应用类模块
提供简洁的 API 用于操作桌面应用程序的 UI 元素
"""

import sys
from typing import List, Optional, Union

from relative_position.config import IS_WINDOWS
from relative_position.elements import Ele, Elements
from relative_position.utils import logger


class App:
    """
    应用类 - 提供简洁的应用程序 UI 元素操作接口

    使用示例：
    ```python
    from relative_position import App

    # 创建应用实例
    app = App(appname="explorer.exe")

    # 使用 app.Ele() 创建元素
    new_file_btn = app.Ele(
        direction="left_top",
        location=[20, 20, 50, 35]
    )

    # 操作元素
    new_file_btn.click()
    new_file_btn.right_click()
    new_file_btn.double_click()
    x, y = new_file_btn.center()
    ```
    """

    def __init__(
        self,
        appname: str,
        number: int = -1,
        pause: int = 1,
        retry: int = 1,
        config_path: Optional[str] = None
    ):
        """
        初始化应用实例

        :param appname: 应用程序名称
            Windows: "explorer.exe", "notepad.exe" 等
            Linux: "gedit", "firefox" 等
        :param number: 窗口索引，默认 -1（最后一个窗口）
        :param pause: 每个操作步骤之前暂停的时间（秒）
        :param retry: 重试次数
        :param config_path: 可选的配置文件路径（已废弃，使用 Elements 对象或字典）
        """
        self.appname = appname
        self.number = number
        self.pause = pause
        self.retry = retry
        self.config_path = config_path

        # 根据平台加载对应的 ButtonCenter
        if IS_WINDOWS:
            from relative_position.windows.main import ButtonCenter as WindowsButtonCenter
            self._button_center = WindowsButtonCenter(
                app_name=appname,
                config_path={},  # 初始化为空字典
                number=number,
                pause=pause,
                retry=retry
            )
        else:
            from relative_position.linux.main import ButtonCenter as LinuxButtonCenter
            self._button_center = LinuxButtonCenter(
                app_name=appname,
                config_path={},  # 初始化为空字典
                number=number,
                pause=pause,
                retry=retry
            )

        # 注册元素列表
        self._elements = Elements()
        self._element_counter = 0

    def add_element(self, name: str, element: Ele):
        """
        添加元素到应用

        :param name: 元素名称
        :param element: Ele 对象
        """
        self._elements.add(name, element)
        # 更新 ButtonCenter 的元素字典
        self._button_center._elements_dict = self._elements.to_dict()

    def register_element(self, element: Ele) -> str:
        """
        自动注册元素并返回元素名称

        :param element: Ele 对象
        :return: 元素名称（自动生成）
        """
        element_name = f"element_{self._element_counter}"
        self._element_counter += 1
        self.add_element(element_name, element)
        return element_name

    def Ele(self, direction: str, location: List[int], name: Optional[str] = None) -> Ele:
        """
        创建并注册元素

        使用示例：
        ```python
        app = App(appname="explorer.exe")

        new_file_btn = app.Ele(
            direction="left_top",
            location=[20, 20, 50, 35]
        )
        new_file_btn.click()
        new_file_btn.right_click()
        new_file_btn.double_click()
        x, y = new_file_btn.center()
        ```

        :param direction: 参考点方向
            可选值: left_bottom, left_top, right_top, right_bottom,
                     top_center, bottom_center, left_center, right_center, window_size
        :param location: 相对位置坐标 [x, y, width, height]
        :param name: 可选的元素名称，用于后续引用
        :return: Ele 对象
        """
        element = Ele(direction=direction, location=location, app=self, name=name)
        return element

    def get_center(self, element: Union[Ele, str]) -> tuple:
        """
        获取元素的中心坐标

        :param element: Ele 对象或元素名称
        :return: (x, y) 坐标
        """
        if isinstance(element, Ele):
            # 如果是 Ele 对象，需要先注册
            element_name = self.register_element(element)
            return self._button_center.btn_center(element_name)
        elif isinstance(element, str):
            # 如果是元素名称，直接获取
            return self._button_center.btn_center(element)
        else:
            raise TypeError(f"不支持的元素类型: {type(element)}")

    def focus_window(self):
        """将应用窗口置顶并聚焦"""
        self._button_center.focus_windows()

    def window_info(self):
        """获取窗口信息"""
        return self._button_center.window_info()

    def window_size(self) -> tuple:
        """获取窗口大小"""
        return self._button_center.window_sizes()

    def window_center(self) -> tuple:
        """获取窗口中心坐标"""
        return self._button_center.window_center()

    def window_position(self) -> tuple:
        """获取窗口左上角坐标"""
        return self._button_center.window_left_top_position()


# 鼠标操作工具函数
class Mouse:
    """鼠标操作类"""

    @staticmethod
    def move_to(x: int, y: int):
        """
        移动鼠标到指定坐标

        :param x: x 坐标
        :param y: y 坐标
        """
        if sys.platform.startswith('win'):
            import ctypes
            ctypes.windll.user32.SetCursorPos(int(x), int(y))
        elif sys.platform.startswith('linux'):
            import subprocess
            subprocess.run(['xdotool', 'mousemove', str(int(x)), str(int(y))], check=False)
        logger.debug(f"鼠标移动到: ({x}, {y})")

    @staticmethod
    def click(button: str = 'left', clicks: int = 1):
        """
        鼠标点击

        :param button: 按钮类型，'left', 'right', 'middle'
        :param clicks: 点击次数
        """
        if sys.platform.startswith('win'):
            import ctypes
            import time

            button_codes = {
                'left': (0x0002, 0x0004),      # MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
                'right': (0x0008, 0x0010),    # MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
                'middle': (0x0020, 0x0040)    # MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP
            }

            if button not in button_codes:
                raise ValueError(f"不支持的按钮类型: {button}")

            down_code, up_code = button_codes[button]

            for _ in range(clicks):
                ctypes.windll.user32.mouse_event(down_code, 0, 0, 0, 0)
                time.sleep(0.05)
                ctypes.windll.user32.mouse_event(up_code, 0, 0, 0, 0)
                if _ < clicks - 1:  # 不是最后一次点击
                    time.sleep(0.1)

        elif sys.platform.startswith('linux'):
            import subprocess
            button_map = {
                'left': '1',
                'right': '3',
                'middle': '2'
            }

            if button not in button_map:
                raise ValueError(f"不支持的按钮类型: {button}")

            for _ in range(clicks):
                subprocess.run(['xdotool', 'click', button_map[button]], check=False)
                if _ < clicks - 1:
                    import time
                    time.sleep(0.1)

        logger.debug(f"鼠标{button}点击 {clicks} 次")

    @staticmethod
    def double_click(button: str = 'left'):
        """
        鼠标双击

        :param button: 按钮类型，默认 'left'
        """
        Mouse.click(button=button, clicks=2)
        logger.debug(f"鼠标{button}双击")
