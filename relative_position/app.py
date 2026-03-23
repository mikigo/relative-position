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
        retry: int = 1
    ):
        """
        初始化应用实例

        :param appname: 应用程序名称
            Windows: "explorer.exe", "notepad.exe" 等
            Linux: "gedit", "firefox" 等
        :param number: 窗口索引，默认 -1（最后一个窗口）
        :param pause: 每个操作步骤之前暂停的时间（秒）
        :param retry: 重试次数
        """
        self.appname = appname
        self.number = number
        self.pause = pause
        self.retry = retry

        # 根据平台加载对应的 RelativePosition
        if IS_WINDOWS:
            from relative_position.windows.main import RelativePosition as WindowsRelativePosition
            self._button_center = WindowsRelativePosition(
                app_name=appname,
                config={},
                number=number,
                pause=pause,
                retry=retry
            )
        else:
            from relative_position.linux.main import RelativePosition as LinuxRelativePosition
            self._button_center = LinuxRelativePosition(
                app_name=appname,
                config={},
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
    """鼠标操作类 - 使用 pyautogui 实现"""

    @staticmethod
    def move_to(x: int, y: int):
        """
        移动鼠标到指定坐标

        :param x: x 坐标
        :param y: y 坐标
        """
        try:
            import pyautogui
            pyautogui.moveTo(int(x), int(y))
            logger.debug(f"鼠标移动到: ({x}, {y})")
        except ImportError:
            raise ImportError(
                "pyautogui 未安装，请运行: pip install pyautogui"
            )

    @staticmethod
    def click(button: str = 'left', clicks: int = 1):
        """
        鼠标点击

        :param button: 按钮类型，'left', 'right', 'middle'
        :param clicks: 点击次数
        """
        try:
            import pyautogui
            pyautogui.click(button=button, clicks=clicks)
            logger.debug(f"鼠标{button}点击 {clicks} 次")
        except ImportError:
            raise ImportError(
                "pyautogui 未安装，请运行: pip install pyautogui"
            )

    @staticmethod
    def double_click(button: str = 'left'):
        """
        鼠标双击

        :param button: 按钮类型，默认 'left'
        """
        try:
            import pyautogui
            pyautogui.doubleClick(button=button)
            logger.debug(f"鼠标{button}双击")
        except ImportError:
            raise ImportError(
                "pyautogui 未安装，请运行: pip install pyautogui"
            )
