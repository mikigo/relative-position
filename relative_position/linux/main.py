#!/usr/bin/env python3
# _*_ coding:utf-8 _*_


import sys
from time import sleep
from typing import Optional, Union

try:
    import dbus
except ImportError:
    dbus = None

from relative_position.config import config
from relative_position.utils import logger, CmdCtl, ShortCut
from relative_position.exceptions import ApplicationStartError, GetWindowInformation
from relative_position.linux.base import ButtonCenterBase
from relative_position.linux.wayland_wininfo import WaylandWindowInfo
from relative_position.linux.x11_wininfo import X11WindowInfo


class ButtonCenter(ButtonCenterBase):
    """
    根据应用程序中控件元素的相对坐标，通过配置元素的x、y、w和h来定位元素在屏幕中的位置，并返回用于鼠标和键盘操作的坐标。

    Linux 平台实现，支持 X11 和 Wayland 两种显示服务器。
    """

    def __init__(
        self, app_name: str, config_path: str, number: int = -1, pause: int = 1, retry: int = 1
    ):
        """
        :param app_name: 系统应用软件包，例如，dde-file-manager
        :param config_path: ui 定位配置文件路径（绝对路径）
        :param number: 默认为 -1, 即最后一个窗口
            如果你想指定不同的窗口，你可以在实例化对象的时候显式的传入 number，第一个为 0
        """
        super().__init__(app_name, config_path, number, pause, retry)
        self._init_window_provider()

    def _init_window_provider(self):
        """根据平台初始化窗口信息提供者"""
        if config.IS_X11:
            self.window_provider = X11WindowInfo()
        elif config.IS_WAYLAND:
            self.window_provider = WaylandWindowInfo()
        else:
            raise RuntimeError(f"不支持的显示服务器: {config.get_display_server()}")

    def window_info(self):
        """
         窗口信息
        :return:  窗口的基本信息，左上角坐标，窗口宽高等
        """
        if config.IS_X11:
            try:
                window_id = self.window_provider.get_window_id_by_index(self.app_name, self.number)
                if window_id is None:
                    raise ApplicationStartError(self.app_name)

                # 获取窗口详细信息
                window_info = self.window_provider._get_window_info_by_id(window_id)
                if not window_info:
                    raise ApplicationStartError(self.app_name)

                return window_info
            except Exception as exc:
                raise ApplicationStartError(f"{self.app_name, exc}") from exc

        elif config.IS_WAYLAND:
            self.wwininfo = WaylandWindowInfo()
            if hasattr(self.wwininfo.library, "GetAllWindowStatesList"):
                for _ in range(self.retry + 1):
                    info = self.wwininfo.window_info().get(self.app_name)
                    if info is None:
                        sleep(1)
                    else:
                        break
                else:
                    raise ApplicationStartError(self.app_name)
                if isinstance(info, dict):
                    return info
                elif isinstance(info, list):
                    return info[self.number]
            else:
                proxy_object = dbus.SessionBus().get_object("org.kde.KWin", "/dde")
                dbus.Interface(proxy_object, "org.kde.KWin").WindowMove()
                sleep(self.pause)
                ShortCut.esc()
                return self.wwininfo._window_info()
        return None

    def window_location_and_sizes(self):
        """
         获取窗口的位置及大小
        :return:
        """
        try:
            if config.IS_X11:
                app_window_info = self.window_info()
                return app_window_info.get("location")
            else:
                self.wwininfo = WaylandWindowInfo()
                if hasattr(self.wwininfo.library, "GetAllWindowStatesList"):
                    app_window_info = self.window_info()
                    window_x, window_y, window_width, window_height = app_window_info.get(
                        "location"
                    )
                else:
                    app_window_info = self.window_info()
                    name = app_window_info.get("name")
                    if name != self.app_name:
                        raise ValueError(
                            f"您想要获取的窗口为：{self.app_name}, 但实际获取的窗口为：{name}"
                        )
                    window_x, window_y, window_width, window_height = app_window_info.get("wininfo")
            logger.debug(
                f"窗口左上角坐标 {window_x, window_y},获取窗口大小 {window_width}*{window_height}"
            )
            return (int(window_x), int(window_y), int(window_width), int(window_height))
        except (IndexError, KeyError) as exc:
            raise GetWindowInformation(f"获取窗口大小错误 {exc}") from exc

    def window_left_top_position(self) -> tuple:
        """
         获取窗口左上角坐标
        :return:  (0, 0)
        """
        try:
            if config.IS_X11:
                app_window_info = self.window_info()
                location = app_window_info.get("location")
                window_x, window_y = location[0], location[1]
            else:
                self.wwininfo = WaylandWindowInfo()
                app_window_info = self.window_info()
                if hasattr(self.wwininfo.library, "GetAllWindowStatesList"):
                    location = app_window_info.get("location")
                    window_x, window_y = location[0], location[1]
                else:
                    window_x, window_y, window_width, window_height = app_window_info.get("wininfo")
            logger.debug(f"窗口左上角坐标 {window_x, window_y}")
            return int(window_x), int(window_y)
        except (ValueError, KeyError) as exc:
            raise GetWindowInformation(f"获取窗口左上角坐标错误 {exc}") from exc

    def window_sizes(self) -> tuple:
        """
         获取窗口的大小
        :return:  (宽， 高)， 例如：(400, 600)
        """
        try:
            if config.IS_X11:
                app_window_info = self.window_info()
                location = app_window_info.get("location")
                window_width = location[2]
                window_height = location[3]
            else:
                self.wwininfo = WaylandWindowInfo()
                app_window_info = self.window_info()
                if hasattr(self.wwininfo.library, "GetAllWindowStatesList"):
                    location = app_window_info.get("location")
                    window_x, window_y, window_width, window_height = location
                else:
                    window_x, window_y, window_width, window_height = app_window_info.get("wininfo")
            logger.debug(f"获取窗口大小 {window_width}*{window_height}")
            return int(window_width), int(window_height)
        except (IndexError, KeyError) as exc:
            raise GetWindowInformation(f"获取窗口大小错误 {exc}") from exc

    def window_left_bottom_position(self) -> tuple:
        """
         左下角的坐标
        :return:  (0, 1080)
        """
        (
            window_x,
            window_y,
            _window_width,
            window_height,
        ) = self.window_location_and_sizes()
        left_y = window_y + window_height
        logger.debug(f"窗口左下角坐标 {window_x, left_y}")
        return int(window_x), int(left_y)

    def window_right_top_position(self) -> tuple:
        """
         右上角的坐标
        :return:  (1920, 0)
        """
        (
            window_x,
            window_y,
            window_width,
            _window_height,
        ) = self.window_location_and_sizes()
        right_x = window_x + window_width
        logger.debug(f"窗口右上角坐标 {right_x, window_y}")
        return int(right_x), int(window_y)

    def window_right_bottom_position(self) -> tuple:
        """
         右下角的坐标
        :return:  (1920, 1080)
        """
        (
            window_x,
            window_y,
            window_width,
            window_height,
        ) = self.window_location_and_sizes()
        right_x = window_x + window_width
        right_y = window_y + window_height
        logger.debug(f"窗口右下角坐标 {right_x, right_y}")
        return int(right_x), int(right_y)

    def window_left_center_position(self) -> tuple:
        """
         获取窗口左边界中心坐标
        :return:  (0, 540)
        """
        (
            window_x,
            window_y,
            _window_width,
            window_height,
        ) = self.window_location_and_sizes()
        center_y = window_y + window_height / 2
        logger.debug(f"窗口左边界中心坐标 {window_x, center_y}")
        return int(window_x), int(center_y)

    def window_top_center_position(self) -> tuple:
        """
         获取窗口上边界中心坐标
        :return:  (960, 0)
        """
        (
            window_x,
            window_y,
            window_width,
            _window_height,
        ) = self.window_location_and_sizes()
        center_x = window_x + window_width / 2
        logger.debug(f"获取窗口上边界中心坐标 {center_x, window_y}")
        return int(center_x), int(window_y)

    def window_right_center_position(self) -> tuple:
        """
         获取窗口右边界中心坐标
        :return:  (1920, 540)
        """
        (
            window_x,
            window_y,
            window_width,
            window_height,
        ) = self.window_location_and_sizes()
        right_x = window_x + window_width
        center_y = window_y + window_height / 2
        logger.debug(f"获取窗口右边界中心坐标 {right_x, center_y}")
        return int(right_x), int(center_y)

    def window_bottom_center_position(self) -> tuple:
        """
         获取窗口下边界中心的坐标
        :return:  (960, 1080)
        """
        (
            window_x,
            window_y,
            window_width,
            window_height,
        ) = self.window_location_and_sizes()
        center_x = window_x + window_width / 2
        bottom_y = window_y + window_height
        logger.debug(f"获取窗口下边界中心的坐标 {center_x, bottom_y}")
        return int(center_x), int(bottom_y)

    def window_center(self) -> tuple:
        """
         获取窗口的中心点坐标
        :return:  (960, 540)
        """
        (
            window_x,
            window_y,
            window_width,
            window_height,
        ) = self.window_location_and_sizes()
        _x = window_x + window_width / 2
        _y = window_y + window_height / 2
        logger.debug(f"窗口中心坐标 {_x, _y}")
        return _x, _y

    def btn_center_by_left_top(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据左上角的坐标按钮的中心坐标
        :param button_x: 控件左上角相对于窗口左上角的横向距离
        :param button_y: 控件左上角相对于窗口左上角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_left_top_position()
        b_x = window_x + button_x + button_w / 2
        b_y = window_y + button_y + button_h / 2
        logger.debug(f"左上角按钮的中心坐标 {b_x, b_y}")
        return b_x, b_y

    def btn_center_by_right_top(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据右上角的坐标按钮的中心坐标
        :param button_x: 控件右上角相对于窗口右上角的横向距离
        :param button_y: 控件右上角相对于窗口右上角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_right_top_position()
        b_x = window_x - button_x - button_w / 2
        b_y = window_y + button_y + button_h / 2
        logger.debug(f"右上角按钮的中心坐标 {b_x, b_y}")
        return b_x, b_y

    def btn_center_by_left_bottom(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据左下角的坐标按钮的中心坐标
        :param button_x: 控件左下角相对于窗口左下角的横向距离
        :param button_y: 控件左下角相对于窗口左下角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_left_bottom_position()
        b_x = window_x + button_x + button_w / 2
        b_y = window_y - button_y - button_h / 2
        logger.debug(f"左下角按钮的中心坐标 {b_x, b_y}")
        return b_x, b_y

    def btn_center_by_right_bottom(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据右下角的坐标按钮的中心坐标
        :param button_x: 控件右下角相对于窗口右下角的横向距离
        :param button_y: 控件右下角相对于窗口右下角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_right_bottom_position()
        b_x = window_x - button_x - button_w / 2
        b_y = window_y - button_y - button_h / 2
        logger.debug(f"右下角按钮的中心坐标 {b_x, b_y}")
        return b_x, b_y

    def btn_pic_by_left_top(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据左上角的坐标按钮的截图区域
        :param button_x: 控件左上角相对于窗口左上角的横向距离
        :param button_y: 控件左上角相对于窗口左上角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_left_top_position()
        b_x = window_x + button_x
        b_y = window_y + button_y
        logger.debug(f"左上角按钮的截取区域左上角 {b_x, b_y}, 控件长宽 {button_w, button_h}")
        return b_x, b_y, button_w, button_h

    def btn_pic_by_right_top(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据右上角的坐标按钮的截图区域
        :param button_x: 控件右上角相对于窗口右上角的横向距离
        :param button_y: 控件右上角相对于窗口右上角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_right_top_position()
        b_x = window_x - button_x - button_w
        b_y = window_y + button_y
        logger.debug(f"右上角按钮的截取区域左上角 {b_x, b_y}, 控件长宽 {button_w, button_h}")
        return b_x, b_y, button_w, button_h

    def btn_pic_by_left_bottom(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据左下角的坐标按钮的截图区域
        :param button_x: 控件左下角相对于窗口左下角的横向距离
        :param button_y: 控件左下角相对于窗口左下角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_left_bottom_position()
        b_x = window_x + button_x
        b_y = window_y - button_y - button_h
        logger.debug(f"左下角按钮的截取区域左上角 {b_x, b_y}, 控件长宽 {button_w, button_h}")
        return b_x, b_y, button_w, button_h

    def btn_pic_by_right_bottom(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据右下角的坐标按钮的截图区域
        :param button_x: 控件右下角相对于窗口右下角的横向距离
        :param button_y: 控件右下角相对于窗口右下角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_right_bottom_position()
        b_x = window_x - button_x - button_w
        b_y = window_y - button_y - button_h
        logger.debug(f"右下角按钮的截取区域左上角 {b_x, b_y}, 控件长宽 {button_w, button_h}")
        return b_x, b_y, button_w, button_h

    def btn_center(
        self,
        btn_name: str,
        offset_x: Optional[Union[int, float]] = None,
        multiplier_x: Optional[Union[int, float]] = None,
        offset_y: Optional[Union[int, float]] = None,
        multiplier_y: Optional[Union[int, float]] = None,
    ) -> tuple:
        """
        获取元素的中心坐标
        :param btn_name: 控件名
        :param offset_x: 正数为右移动，负数为左移动
        :param multiplier_x: offset_x 移动的倍数
        :param offset_y: 正数为上移动，负数为下移动
        :param multiplier_y: offset_y 移动的倍数
        :return: 元素中心坐标 (x, y)
        """
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
            logger.debug(f"[{btn_name}] 坐标：{str(btn_x)}, {str(btn_y)})")
            return btn_x, btn_y

        raise ValueError(
            f"{direction}, 默认参考点 {default_point + default_boundary_point}"
        )

    def btn_size(
        self,
        btn_name: str,
        offset_x: Optional[Union[int, float]] = None,
        multiplier_x: Optional[Union[int, float]] = None,
        offset_y: Optional[Union[int, float]] = None,
        multiplier_y: Optional[Union[int, float]] = None,
    ) -> tuple:
        """
        获取元素的左上角坐标及长宽
        :param btn_name: 控件名
        :param offset_x: 正数为右移动，负数为左移动
        :param multiplier_x: offset_x 移动的倍数
        :param offset_y: 正数为上移动，负数为下移动
        :param multiplier_y: offset_y 移动的倍数
        :return: (x, y, width, height)
        """
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
            logger.debug(
                f"[{btn_name}] 左上角坐标：{str(btn_x)}, {str(btn_y)}), 长宽 {button_w, button_h}"
            )
            return btn_x, btn_y, button_w, button_h

        raise ValueError(
            f"{direction}, 默认参考点 {default_point + default_boundary_point}"
        )

    def btn_info(self, btn_name: str) -> tuple:
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

    def get_windows_number(self, name: str) -> int:
        """
         获取应用所有窗口数量
        :param name: 应用包名
        :return: int 窗口数量
        """
        if config.IS_X11:
            info = self.window_provider.get_windows_by_name(name)
            if info is None:
                return 0
            elif isinstance(info, dict):
                return 1
            elif isinstance(info, list):
                return len(info)
            return 0
        else:
            info = WaylandWindowInfo().window_info().get(self.app_name)
            if isinstance(info, dict):
                return 1
            elif isinstance(info, list):
                return len(info)
            return 0

    def get_windows_id(self, name: str) -> list:
        """
         获取活动应用窗口ID
        :param name: 应用包名
        :return: 窗口编号列表
        """
        if config.IS_X11:
            info = self.window_provider.get_windows_by_name(name)
            if info is None:
                raise ApplicationStartError(name)
            elif isinstance(info, dict):
                return [info.get("window_id")]
            elif isinstance(info, list):
                return [i.get("window_id") for i in info]
            return []
        else:
            info = self.wwininfo.window_info().get(self.app_name)
            if isinstance(info, dict):
                return info.get("window_id")
            elif isinstance(info, list):
                return [i.get("window_id") for i in info]
            return []

    def focus_windows(self, app_name: str = None):
        """
         窗口置顶并聚焦
        :param app_name: 应用包名
        """
        app_name = app_name if app_name else self.app_name

        if config.IS_WAYLAND:
            return

        window_id = self.window_provider.get_window_id_by_index(app_name, self.number)
        if window_id:
            self.window_provider.focus_window(window_id)
            logger.debug(f"<{app_name}> 窗口置顶并聚焦")

    def get_lastest_window_id(self, app_name: str) -> int:
        """
         获取应用的所有窗口编号，并返回编号最大的窗口ID
        :return: 返回最新创建的窗口编号
        """
        if config.IS_X11:
            window_id = self.window_provider.get_window_id_by_index(app_name, -1)
            if window_id is None:
                raise ApplicationStartError(app_name)
            return int(window_id)
        else:
            info = WaylandWindowInfo().window_info().get(self.app_name)
            if isinstance(info, dict):
                return info.get("window_id")
            elif isinstance(info, list):
                return info[-1].get("window_id")
            raise ApplicationStartError(app_name)
