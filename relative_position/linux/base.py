#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
Linux 平台基类模块
定义统一的接口，支持 X11 和 Wayland 实现
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional


class WindowInfoProvider(ABC):
    """窗口信息提供者抽象基类"""

    @abstractmethod
    def window_info(self) -> Dict:
        """
        获取所有窗口信息
        :return: 字典，key为进程名，value为窗口信息列表或单个窗口信息
        """
        pass

    @abstractmethod
    def get_windows_by_name(self, app_name: str) -> Optional[Dict]:
        """
        根据应用名称获取窗口信息
        :param app_name: 应用名称
        :return: 窗口信息字典或列表
        """
        pass


class ButtonCenterBase(ABC):
    """
    按钮中心抽象基类
    根据应用程序中控件元素的相对坐标，通过配置元素的x、y、w和h来定位元素在屏幕中的位置
    """

    def __init__(self, app_name: str, config_path, number: int = -1, pause: int = 1, retry: int = 1):
        """
        :param app_name: 系统应用软件包
        :param config_path: ui 定位配置文件路径（绝对路径）或 Elements 对象
        :param number: 默认为 -1, 即最后一个窗口
            如果你想指定不同的窗口，你可以在实例化对象的时候显式的传入 number，第一个为 0
        :param pause: 每个操作步骤之前暂停的时间
        :param retry: 重试次数
        """
        self.app_name = app_name
        self.number = number
        self.pause = pause
        self.config_path = config_path
        self.retry = retry
        self._elements_dict = self._parse_config(config_path)

    def _parse_config(self, config):
        """
        解析配置，支持 Ele 对象和 INI 文件

        :param config: 配置文件路径或 Elements 对象
        :return: 元素字典
        """
        from relative_position.elements import Elements

        if isinstance(config, Elements):
            return config.to_dict()
        elif isinstance(config, str):
            from configparser import ConfigParser
            conf = ConfigParser()
            conf.read(config)
            result = {}
            for section in conf.sections():
                result[section] = {
                    'direction': conf.get(section, 'direction'),
                    'location': [int(i.strip()) for i in conf.get(section, 'location').split(',')]
                }
            return result
        elif isinstance(config, dict):
            return config
        else:
            raise ValueError(f"不支持的配置类型: {type(config)}. "
                           "请提供 Ele 对象、Elements 对象、INI 文件路径或字典")
        self._elements_dict = self._parse_config(config_path)

    @abstractmethod
    def window_info(self):
        """
        窗口信息
        :return: 窗口的基本信息，左上角坐标，窗口宽高等
        """
        pass

    @abstractmethod
    def window_location_and_sizes(self) -> Tuple[int, int, int, int]:
        """
        获取窗口的位置及大小
        :return: (x, y, width, height)
        """
        pass

    @abstractmethod
    def window_left_top_position(self) -> Tuple[int, int]:
        """
        获取窗口左上角坐标
        :return: (x, y)
        """
        pass

    @abstractmethod
    def window_sizes(self) -> Tuple[int, int]:
        """
        获取窗口的大小
        :return: (宽， 高)， 例如：(400, 600)
        """
        pass

    def window_left_bottom_position(self) -> Tuple[int, int]:
        """
        左下角的坐标
        :return: (x, y)
        """
        window_x, window_y, _window_width, window_height = self.window_location_and_sizes()
        left_y = window_y + window_height
        return int(window_x), int(left_y)

    def window_right_top_position(self) -> Tuple[int, int]:
        """
        右上角的坐标
        :return: (x, y)
        """
        window_x, window_y, window_width, _window_height = self.window_location_and_sizes()
        right_x = window_x + window_width
        return int(right_x), int(window_y)

    def window_right_bottom_position(self) -> Tuple[int, int]:
        """
        右下角的坐标
        :return: (x, y)
        """
        window_x, window_y, window_width, window_height = self.window_location_and_sizes()
        right_x = window_x + window_width
        right_y = window_y + window_height
        return int(right_x), int(right_y)

    def window_left_center_position(self) -> Tuple[int, int]:
        """
        获取窗口左边界中心坐标
        :return: (x, y)
        """
        window_x, window_y, _window_width, window_height = self.window_location_and_sizes()
        center_y = window_y + window_height / 2
        return int(window_x), int(center_y)

    def window_top_center_position(self) -> Tuple[int, int]:
        """
        获取窗口上边界中心坐标
        :return: (x, y)
        """
        window_x, window_y, window_width, _window_height = self.window_location_and_sizes()
        center_x = window_x + window_width / 2
        return int(center_x), int(window_y)

    def window_right_center_position(self) -> Tuple[int, int]:
        """
        获取窗口右边界中心坐标
        :return: (x, y)
        """
        window_x, window_y, window_width, window_height = self.window_location_and_sizes()
        right_x = window_x + window_width
        center_y = window_y + window_height / 2
        return int(right_x), int(center_y)

    def window_bottom_center_position(self) -> Tuple[int, int]:
        """
        获取窗口下边界中心的坐标
        :return: (x, y)
        """
        window_x, window_y, window_width, window_height = self.window_location_and_sizes()
        center_x = window_x + window_width / 2
        bottom_y = window_y + window_height
        return int(center_x), int(bottom_y)

    def window_center(self) -> Tuple[float, float]:
        """
        获取窗口的中心点坐标
        :return: (x, y)
        """
        window_x, window_y, window_width, window_height = self.window_location_and_sizes()
        _x = window_x + window_width / 2
        _y = window_y + window_height / 2
        return _x, _y

    def btn_center_by_left_top(self, button_x: int, button_y: int, button_w: int, button_h: int) -> Tuple[float, float]:
        """
        根据左上角的坐标按钮的中心坐标
        :param button_x: 控件左上角相对于窗口左上角的横向距离
        :param button_y: 控件左上角相对于窗口左上角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return: 控件的中心坐标 (x, y)
        """
        window_x, window_y = self.window_left_top_position()
        b_x = window_x + button_x + button_w / 2
        b_y = window_y + button_y + button_h / 2
        return b_x, b_y

    def btn_center_by_right_top(self, button_x: int, button_y: int, button_w: int, button_h: int) -> Tuple[float, float]:
        """
        根据右上角的坐标按钮的中心坐标
        :param button_x: 控件右上角相对于窗口右上角的横向距离
        :param button_y: 控件右上角相对于窗口右上角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return: 控件的中心坐标 (x, y)
        """
        window_x, window_y = self.window_right_top_position()
        b_x = window_x - button_x - button_w / 2
        b_y = window_y + button_y + button_h / 2
        return b_x, b_y

    def btn_center_by_left_bottom(self, button_x: int, button_y: int, button_w: int, button_h: int) -> Tuple[float, float]:
        """
        根据左下角的坐标按钮的中心坐标
        :param button_x: 控件左下角相对于窗口左下角的横向距离
        :param button_y: 控件左下角相对于窗口左下角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return: 控件的中心坐标 (x, y)
        """
        window_x, window_y = self.window_left_bottom_position()
        b_x = window_x + button_x + button_w / 2
        b_y = window_y - button_y - button_h / 2
        return b_x, b_y

    def btn_center_by_right_bottom(self, button_x: int, button_y: int, button_w: int, button_h: int) -> Tuple[float, float]:
        """
        根据右下角的坐标按钮的中心坐标
        :param button_x: 控件右下角相对于窗口右下角的横向距离
        :param button_y: 控件右下角相对于窗口右下角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return: 控件的中心坐标 (x, y)
        """
        window_x, window_y = self.window_right_bottom_position()
        b_x = window_x - button_x - button_w / 2
        b_y = window_y - button_y - button_h / 2
        return b_x, b_y

    def btn_pic_by_left_top(self, button_x: int, button_y: int, button_w: int, button_h: int) -> Tuple[int, int, int, int]:
        """
        根据左上角的坐标按钮的截图区域
        :param button_x: 控件左上角相对于窗口左上角的横向距离
        :param button_y: 控件左上角相对于窗口左上角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return: 控件的截图区域 (x, y, w, h)
        """
        window_x, window_y = self.window_left_top_position()
        b_x = window_x + button_x
        b_y = window_y + button_y
        return b_x, b_y, button_w, button_h

    def btn_pic_by_right_top(self, button_x: int, button_y: int, button_w: int, button_h: int) -> Tuple[int, int, int, int]:
        """
        根据右上角的坐标按钮的截图区域
        :param button_x: 控件右上角相对于窗口右上角的横向距离
        :param button_y: 控件右上角相对于窗口右上角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return: 控件的截图区域 (x, y, w, h)
        """
        window_x, window_y = self.window_right_top_position()
        b_x = window_x - button_x - button_w
        b_y = window_y + button_y
        return b_x, b_y, button_w, button_h

    def btn_pic_by_left_bottom(self, button_x: int, button_y: int, button_w: int, button_h: int) -> Tuple[int, int, int, int]:
        """
        根据左下角的坐标按钮的截图区域
        :param button_x: 控件左下角相对于窗口左下角的横向距离
        :param button_y: 控件左下角相对于窗口左下角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return: 控件的截图区域 (x, y, w, h)
        """
        window_x, window_y = self.window_left_bottom_position()
        b_x = window_x + button_x
        b_y = window_y - button_y - button_h
        return b_x, b_y, button_w, button_h

    def btn_pic_by_right_bottom(self, button_x: int, button_y: int, button_w: int, button_h: int) -> Tuple[int, int, int, int]:
        """
        根据右下角的坐标按钮的截图区域
        :param button_x: 控件右下角相对于窗口右下角的横向距离
        :param button_y: 控件右下角相对于窗口右下角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return: 控件的截图区域 (x, y, w, h)
        """
        window_x, window_y = self.window_right_bottom_position()
        b_x = window_x - button_x - button_w
        b_y = window_y - button_y - button_h
        return b_x, b_y, button_w, button_h

    def btn_center(
        self,
        btn_name: str,
        offset_x: Optional[int] = None,
        multiplier_x: Optional[int] = None,
        offset_y: Optional[int] = None,
        multiplier_y: Optional[int] = None,
    ) -> Tuple[float, float]:
        """
        获取元素的中心坐标
        :param btn_name: 控件名
        :param offset_x: 正数为右移动，负数为左移动
        :param multiplier_x: offset_x 移动的倍数
        :param offset_y: 正数为上移动，负数为下移动
        :param multiplier_y: offset_y 移动的倍数
        :return: 元素中心坐标 (x, y)
        """
        from time import sleep

        btn_x = btn_y = ""
        sleep(self.pause)

        if btn_name not in self._elements_dict:
            raise ValueError(f"元素 '{btn_name}' 未在配置中找到")

        element_config = self._elements_dict[btn_name]
        direction = element_config['direction']
        position = element_config['location']

        default_point = ("left_bottom", "left_top", "right_top", "right_bottom")
        default_boundary_point = (
            "top_center",
            "bottom_center",
            "left_center",
            "right_center",
        )

        if direction in default_point:
            btn_x, btn_y = getattr(self, f"btn_center_by_{direction}")(*position)
        elif direction in default_boundary_point:
            window_x, window_y = getattr(self, f"window_{direction}_position")()
            btn_x = window_x + position[0] + (position[2] / 2 if position[0] > 0 else -position[2] / 2)
            btn_y = window_y + position[1] + (position[3] / 2 if position[1] > 0 else -position[3] / 2)
        elif direction == "window_size":
            btn_x, btn_y, button_w, button_h = self.window_location_and_sizes()
            btn_x = btn_x + button_w / 2
            btn_y = btn_y + button_h / 2

        if btn_x and btn_y:
            if offset_x:
                btn_x = btn_x + int(offset_x) * (int(multiplier_x) if multiplier_x else 1)
            if offset_y:
                btn_y = btn_y + int(offset_y) * (int(multiplier_y) if multiplier_y else 1)
            return btn_x, btn_y

        raise ValueError(
            f"{direction}, 默认参考点 {default_point + default_boundary_point}"
        )

    def btn_size(
        self,
        btn_name: str,
        offset_x: Optional[int] = None,
        multiplier_x: Optional[int] = None,
        offset_y: Optional[int] = None,
        multiplier_y: Optional[int] = None,
    ) -> Tuple[int, int, int, int]:
        """
        获取元素的左上角坐标及长宽
        :param btn_name: 控件名
        :param offset_x: 正数为右移动，负数为左移动
        :param multiplier_x: offset_x 移动的倍数
        :param offset_y: 正数为上移动，负数为下移动
        :param multiplier_y: offset_y 移动的倍数
        :return: (x, y, width, height)
        """
        from time import sleep

        btn_x = btn_y = button_w = button_h = ""
        sleep(self.pause)

        if btn_name not in self._elements_dict:
            raise ValueError(f"元素 '{btn_name}' 未在配置中找到")

        element_config = self._elements_dict[btn_name]
        direction = element_config['direction']
        position = element_config['location']

        default_point = ("left_bottom", "left_top", "right_top", "right_bottom")
        default_boundary_point = (
            "top_center",
            "bottom_center",
            "left_center",
            "right_center",
        )

        if direction in default_point:
            btn_x, btn_y, button_w, button_h = getattr(self, f"btn_pic_by_{direction}")(*position)
        elif direction in default_boundary_point:
            window_x, window_y = getattr(self, f"window_{direction}_position")()
            btn_x = window_x + position[0] - (0 if position[0] > 0 else position[2])
            btn_y = window_y + position[1] - (0 if position[1] > 0 else position[3])
            button_w, button_h = position[2], position[3]
        elif direction == "window_size":
            btn_x, btn_y, button_w, button_h = self.window_location_and_sizes()

        if btn_x != "" and btn_y != "":
            if offset_x:
                btn_x = btn_x + int(offset_x) * (int(multiplier_x) if multiplier_x else 1)
            if offset_y:
                btn_y = btn_y + int(offset_y) * (int(multiplier_y) if multiplier_y else 1)
            return btn_x, btn_y, button_w, button_h

        raise ValueError(
            f"{direction}, 默认参考点 {default_point + default_boundary_point}"
        )

    def btn_info(self, btn_name: str) -> Tuple[list, str]:
        """
        元素的相对位置和参考系
        :param btn_name: 控件名称
        :return: (相对坐标，参考系）
        """
        if btn_name not in self._elements_dict:
            raise ValueError(f"元素 '{btn_name}' 未在配置中找到")

        element_config = self._elements_dict[btn_name]
        direction = element_config['direction']
        position = element_config['location']
        return position, direction

    @abstractmethod
    def get_windows_number(self, name: str) -> int:
        """
        获取应用所有窗口数量
        :param name: 应用包名
        :return: int 窗口数量
        """
        pass

    @abstractmethod
    def get_windows_id(self, name: str) -> List:
        """
        获取活动应用窗口ID
        :param name: 应用包名
        :return: 窗口编号列表
        """
        pass

    @abstractmethod
    def focus_windows(self, app_name: str = None):
        """
        窗口置顶并聚焦
        :param app_name: 应用包名
        """
        pass

    @abstractmethod
    def get_lastest_window_id(self, app_name: str) -> int:
        """
        获取应用的所有窗口编号，并返回编号最大的窗口ID
        :return: 返回最新创建的窗口编号
        """
        pass
