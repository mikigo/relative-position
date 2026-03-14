#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
相对元素定位 - 获取桌面应用中元素在屏幕中的坐标

支持平台:
- Linux (X11 和 Wayland)
- Windows
"""

from relative_position.config import config, IS_WAYLAND, IS_X11, IS_WINDOWS
from relative_position.exceptions import (
    ApplicationStartError,
    ApplicationError,
    GetWindowInformation
)
from relative_position.utils import logger, CmdCtl, ShortCut
from relative_position.elements import Ele, Elements


def get_button_center(app_name: str, config_path: str, **kwargs):
    """
    根据平台获取 ButtonCenter 实例的工厂函数

    :param app_name: 应用程序名称
    :param config_path: 配置文件路径
    :param kwargs: 其他参数（如 number, pause, retry）
    :return: ButtonCenter 实例
    """
    from relative_position.linux.main import ButtonCenter as LinuxButtonCenter
    from relative_position.windows.main import ButtonCenter as WindowsButtonCenter

    if IS_WINDOWS:
        return WindowsButtonCenter(app_name, config_path, **kwargs)
    else:
        return LinuxButtonCenter(app_name, config_path, **kwargs)


def get_window_info_provider():
    """
    根据平台获取窗口信息提供者

    :return: 窗口信息提供者实例
    """
    if IS_WINDOWS:
        from relative_position.windows.windows_wininfo import WindowsWindowInfo
        return WindowsWindowInfo()
    elif IS_X11:
        from relative_position.linux.x11_wininfo import X11WindowInfo
        return X11WindowInfo()
    elif IS_WAYLAND:
        from relative_position.linux.wayland_wininfo import WaylandWindowInfo
        return WaylandWindowInfo()
    else:
        raise RuntimeError(f"不支持的显示服务器: {config.get_display_server()}")


__all__ = [
    'config',
    'IS_WAYLAND',
    'IS_X11',
    'IS_WINDOWS',
    'ApplicationStartError',
    'ApplicationError',
    'GetWindowInformation',
    'logger',
    'CmdCtl',
    'ShortCut',
    'Ele',
    'Elements',
    'get_button_center',
    'get_window_info_provider',
]
