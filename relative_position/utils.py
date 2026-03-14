#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import logging
import sys
from pathlib import Path


def get_logger(name=None):
    """获取logger实例"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger


# 创建默认logger
logger = get_logger(__name__)


class CmdCtl:
    """命令行控制类"""

    @staticmethod
    def run_cmd(cmd, interrupt=True, out_debug_flag=True, command_log=True):
        """
        执行命令并返回输出
        :param cmd: 命令
        :param interrupt: 是否中断
        :param out_debug_flag: 是否输出调试信息
        :param command_log: 是否记录命令日志
        :return: 命令输出
        """
        import subprocess
        if command_log:
            logger.debug(f"执行命令: {cmd}")
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                check=False
            )
            if out_debug_flag:
                logger.debug(f"命令输出: {result.stdout}")
            if result.returncode != 0:
                if interrupt:
                    raise RuntimeError(f"命令执行失败: {cmd}, 错误: {result.stderr}")
            return result.stdout
        except Exception as e:
            if interrupt:
                raise RuntimeError(f"命令执行异常: {cmd}, 错误: {e}") from e
            return ""


class ShortCut:
    """快捷键类"""

    @staticmethod
    def esc():
        """按下ESC键"""
        import subprocess
        if sys.platform.startswith('linux'):
            subprocess.run(['xdotool', 'key', 'Escape'], check=False)
        elif sys.platform.startswith('win'):
            # Windows 实现
            import ctypes
            VK_ESCAPE = 0x1B
            ctypes.windll.user32.keybd_event(VK_ESCAPE, 0, 0, 0)  # 按下
            ctypes.windll.user32.keybd_event(VK_ESCAPE, 0, 2, 0)  # 释放

    @staticmethod
    def press_key(key_code: int):
        """
        按下指定键
        :param key_code: 虚拟键码
        """
        import ctypes
        if sys.platform.startswith('win'):
            ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)  # 按下
            ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)  # 释放


def create_directory(path):
    """创建目录"""
    Path(path).mkdir(parents=True, exist_ok=True)
