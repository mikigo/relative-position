#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import sys
import os


class GlobalConfig:
    """全局配置"""

    @staticmethod
    def _get_display_server():
        """获取显示服务器类型"""
        if sys.platform.startswith('win'):
            return 'windows'
        elif sys.platform.startswith('linux'):
            # 检查是否是Wayland
            session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
            if session_type == 'wayland':
                return 'wayland'
            else:
                return 'x11'
        else:
            return 'unknown'

    @classmethod
    def get_display_server(cls):
        """获取显示服务器类型"""
        if not hasattr(cls, '_display_server'):
            cls._display_server = cls._get_display_server()
        return cls._display_server

    @property
    def IS_WAYLAND(self):
        """是否是Wayland"""
        return self.get_display_server() == 'wayland'

    @property
    def IS_X11(self):
        """是否是X11"""
        return self.get_display_server() == 'x11'

    @property
    def IS_WINDOWS(self):
        """是否是Windows"""
        return self.get_display_server() == 'windows'


# 创建全局实例
config = GlobalConfig()
IS_WAYLAND = config.IS_WAYLAND
IS_X11 = config.IS_X11
IS_WINDOWS = config.IS_WINDOWS
DTK_DISPLAY = False
