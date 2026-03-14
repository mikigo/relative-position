#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
相对元素定位 - 获取桌面应用中元素在屏幕中的坐标

支持平台:
- Linux (X11 和 Wayland)
- Windows
"""

from relative_position.elements import Ele
from relative_position.app import App, Mouse


__all__ = [
    'Ele',
    'App',
    'Mouse',
]
