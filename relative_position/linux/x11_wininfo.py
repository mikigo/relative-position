#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
X11 窗口信息获取模块
使用 xdotool 和 xwininfo 命令获取 X11 窗口信息
"""

import re
from typing import Dict, List, Optional

from relative_position.linux.base import WindowInfoProvider
from relative_position.utils import CmdCtl, logger


class X11WindowInfo(WindowInfoProvider):
    """X11 窗口信息提供者"""

    def __init__(self):
        """初始化 X11 窗口信息提供者"""
        self._check_dependencies()

    def _check_dependencies(self):
        """检查 X11 依赖是否安装"""
        try:
            CmdCtl.run_cmd("which xdotool", interrupt=False, out_debug_flag=False, command_log=False)
        except RuntimeError:
            raise RuntimeError("xdotool 未安装，请先安装: sudo apt-get install xdotool")

        try:
            CmdCtl.run_cmd("which xwininfo", interrupt=False, out_debug_flag=False, command_log=False)
        except RuntimeError:
            raise RuntimeError("xwininfo 未安装，请先安装: sudo apt-get install x11-utils")

    def window_info(self) -> Dict:
        """
        获取所有窗口信息
        :return: 字典，key为进程名，value为窗口信息列表或单个窗口信息
        """
        result = {}

        # 获取所有可见窗口的 ID
        try:
            cmd = "xdotool search --onlyvisible"
            window_ids = CmdCtl.run_cmd(cmd, interrupt=False, out_debug_flag=False, command_log=False)
            window_ids = [wid for wid in window_ids.strip().split('\n') if wid]

            for window_id in window_ids:
                try:
                    info = self._get_window_info_by_id(window_id)
                    if info:
                        process_name = info.get('process_name', '')
                        if process_name:
                            if process_name not in result:
                                result[process_name] = info
                            else:
                                if isinstance(result[process_name], dict):
                                    result[process_name] = [result[process_name], info]
                                elif isinstance(result[process_name], list):
                                    result[process_name].append(info)
                except Exception as e:
                    logger.debug(f"获取窗口 {window_id} 信息失败: {e}")
                    continue
        except Exception as e:
            logger.error(f"获取窗口信息失败: {e}")

        return result

    def _get_window_info_by_id(self, window_id: str) -> Optional[Dict]:
        """
        根据窗口 ID 获取窗口信息
        :param window_id: 窗口 ID
        :return: 窗口信息字典
        """
        try:
            # 获取窗口详细信息
            cmd = f"xwininfo -id {window_id}"
            window_info = CmdCtl.run_cmd(cmd, interrupt=False, out_debug_flag=False, command_log=False)

            # 解析窗口信息
            re_pattern = re.compile(r"Absolute.*:\s\s(-?\d+)")
            result = re.findall(re_pattern, window_info)

            if not result or len(result) < 2:
                return None

            window_x, window_y = result
            window_width = re.findall(r"Width.*:\s(\d+)", window_info)
            window_height = re.findall(r"Height.*:\s(\d+)", window_info)

            if not window_width or not window_height:
                return None

            # 获取窗口 PID
            pid_cmd = f"xdotool getwindowpid {window_id}"
            try:
                pid = CmdCtl.run_cmd(pid_cmd, interrupt=False, out_debug_flag=False, command_log=False).strip()
            except:
                pid = "0"

            # 获取进程名称
            process_name = ""
            if pid:
                try:
                    process_name_cmd = f"cat /proc/{pid}/comm"
                    process_name = CmdCtl.run_cmd(
                        process_name_cmd, interrupt=False, out_debug_flag=False, command_log=False
                    ).strip()
                except:
                    pass

            return {
                "window_id": window_id,
                "pid": int(pid) if pid else 0,
                "process_name": process_name,
                "location": (int(window_x), int(window_y), int(window_width[0]), int(window_height[0])),
            }
        except Exception as e:
            logger.debug(f"解析窗口信息失败: {e}")
            return None

    def get_windows_by_name(self, app_name: str) -> Optional[Dict]:
        """
        根据应用名称获取窗口信息
        :param app_name: 应用名称
        :return: 窗口信息字典或列表
        """
        try:
            # 获取窗口 ID 列表
            cmd = f"xdotool search --classname --onlyvisible {app_name}"
            app_id = CmdCtl.run_cmd(cmd, interrupt=False, out_debug_flag=False, command_log=False)
            app_id_list = [int(_id) for _id in app_id.strip().split('\n') if _id]
            app_id_list.sort()

            if not app_id_list:
                return None
            elif len(app_id_list) == 1:
                return self._get_window_info_by_id(str(app_id_list[0]))
            else:
                return [self._get_window_info_by_id(str(wid)) for wid in app_id_list]
        except Exception as e:
            logger.error(f"获取应用 {app_name} 窗口信息失败: {e}")
            return None

    def get_window_id_by_index(self, app_name: str, index: int = -1) -> Optional[str]:
        """
        根据应用名称和索引获取窗口 ID
        :param app_name: 应用名称
        :param index: 窗口索引，默认为 -1（最后一个窗口）
        :return: 窗口 ID
        """
        try:
            cmd = f"xdotool search --classname --onlyvisible {app_name}"
            app_id = CmdCtl.run_cmd(cmd, interrupt=False, out_debug_flag=False, command_log=False)
            app_id_list = [int(_id) for _id in app_id.strip().split('\n') if _id]
            app_id_list.sort()

            if not app_id_list:
                return None

            if index < 0:
                index = len(app_id_list) + index

            if 0 <= index < len(app_id_list):
                return str(app_id_list[index])

            return None
        except Exception as e:
            logger.error(f"获取应用 {app_name} 窗口 ID 失败: {e}")
            return None

    def focus_window(self, window_id: str):
        """
        聚焦指定窗口
        :param window_id: 窗口 ID
        """
        try:
            cmd = f"xdotool windowactivate {window_id}"
            CmdCtl.run_cmd(cmd, interrupt=False, out_debug_flag=False, command_log=False)
        except Exception as e:
            logger.error(f"聚焦窗口 {window_id} 失败: {e}")


if __name__ == "__main__":
    # 测试代码
    xwininfo = X11WindowInfo()
    print("所有窗口信息:")
    windows = xwininfo.window_info()
    for name, info in windows.items():
        print(f"\n应用: {name}")
        if isinstance(info, dict):
            print(f"  位置: {info['location']}")
            print(f"  窗口ID: {info['window_id']}")
        elif isinstance(info, list):
            for i, window_info in enumerate(info):
                print(f"  窗口 {i + 1}:")
                print(f"    位置: {window_info['location']}")
                print(f"    窗口ID: {window_info['window_id']}")
