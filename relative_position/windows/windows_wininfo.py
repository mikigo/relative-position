#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
Windows窗口信息获取模块
使用Windows API获取窗口信息
"""

import ctypes
from ctypes import wintypes
import psutil


# 定义Windows API所需的常量和结构体
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# 定义Windows API常量
WM_GETTEXT = 0x000D
WM_GETTEXTLENGTH = 0x000E
GW_OWNER = 4
GW_HWNDNEXT = 2

# 定义RECT结构体
class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top


# 定义WINDOWINFO结构体
class WINDOWINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcWindow", RECT),
        ("rcClient", RECT),
        ("dwStyle", wintypes.DWORD),
        ("dwExStyle", wintypes.DWORD),
        ("dwWindowStatus", wintypes.DWORD),
        ("cxWindowBorders", wintypes.UINT),
        ("cyWindowBorders", wintypes.UINT),
        ("atomWindowType", wintypes.ATOM),
        ("wCreatorVersion", wintypes.WORD),
    ]


# 定义回调函数类型用于枚举窗口
WNDENUMPROC = ctypes.WINFUNCTYPE(
    ctypes.wintypes.BOOL,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LPARAM
)


class WindowsWindowInfo:
    """获取Windows窗口信息"""

    def __init__(self):
        """初始化Windows窗口信息获取器"""
        self.windows_cache = {}

    def get_window_handle_by_process_name(self, process_name):
        """
        根据进程名获取窗口句柄列表
        :param process_name: 进程名称（不含.exe）
        :return: 窗口句柄列表
        """
        handles = []

        def enum_windows_callback(hwnd, lparam):
            """枚举窗口回调函数"""
            # 检查窗口是否可见
            if not user32.IsWindowVisible(hwnd):
                return True

            # 获取窗口所属进程ID
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

            try:
                process = psutil.Process(pid.value)
                if process_name.lower() in process.name().lower():
                    handles.append(hwnd)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            return True

        callback = WNDENUMPROC(enum_windows_callback)
        user32.EnumWindows(callback, 0)
        return handles

    def get_window_title(self, hwnd):
        """
        获取窗口标题
        :param hwnd: 窗口句柄
        :return: 窗口标题
        """
        length = user32.SendMessageW(hwnd, WM_GETTEXTLENGTH, 0, 0) + 1
        buffer = ctypes.create_unicode_buffer(length)
        user32.SendMessageW(hwnd, WM_GETTEXT, length, ctypes.byref(buffer))
        return buffer.value

    def get_window_class_name(self, hwnd):
        """
        获取窗口类名
        :param hwnd: 窗口句柄
        :return: 窗口类名
        """
        length = 256
        buffer = ctypes.create_unicode_buffer(length)
        user32.GetClassNameW(hwnd, buffer, length)
        return buffer.value

    def get_window_rect(self, hwnd):
        """
        获取窗口矩形区域
        :param hwnd: 窗口句柄
        :return: RECT对象
        """
        rect = RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        return rect

    def get_window_info(self, hwnd):
        """
        获取窗口详细信息
        :param hwnd: 窗口句柄
        :return: 窗口信息字典
        """
        rect = self.get_window_rect(hwnd)

        # 获取进程ID
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        # 获取进程信息
        process_name = ""
        try:
            process = psutil.Process(pid.value)
            process_name = process.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

        # 检查窗口状态
        is_minimized = user32.IsIconic(hwnd)
        is_maximized = user32.IsZoomed(hwnd)
        is_active = user32.GetForegroundWindow() == hwnd

        return {
            "location": (rect.left, rect.top, rect.width, rect.height),
            "title": self.get_window_title(hwnd),
            "class_name": self.get_window_class_name(hwnd),
            "pid": pid.value,
            "process_name": process_name,
            "window_id": hwnd,
            "is_minimized": is_minimized,
            "is_full_screen": is_maximized,
            "is_active": is_active,
        }

    def window_info(self):
        """
        获取所有窗口信息
        :return: 字典，key为进程名，value为窗口信息列表或单个窗口信息
        """
        result = {}

        def enum_windows_callback(hwnd, lparam):
            """枚举窗口回调函数"""
            # 检查窗口是否可见
            if not user32.IsWindowVisible(hwnd):
                return True

            # 排除没有标题的窗口
            title = self.get_window_title(hwnd)
            if not title:
                return True

            # 获取窗口所属进程ID
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

            # 获取进程名
            process_name = ""
            try:
                process = psutil.Process(pid.value)
                process_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return True

            # 获取窗口信息
            info = self.get_window_info(hwnd)

            # 存储窗口信息
            if process_name not in result:
                result[process_name] = info
            else:
                if isinstance(result[process_name], dict):
                    result[process_name] = [result[process_name], info]
                elif isinstance(result[process_name], list):
                    result[process_name].append(info)

            return True

        callback = WNDENUMPROC(enum_windows_callback)
        user32.EnumWindows(callback, 0)

        return result

    def get_windows_by_name(self, app_name):
        """
        根据应用名称获取窗口信息
        :param app_name: 应用名称
        :return: 窗口信息字典或列表
        """
        handles = self.get_window_handle_by_process_name(app_name)

        if not handles:
            return None

        if len(handles) == 1:
            return self.get_window_info(handles[0])
        else:
            return [self.get_window_info(hwnd) for hwnd in handles]

    def get_window_by_index(self, app_name, index=-1):
        """
        根据应用名称和索引获取窗口信息
        :param app_name: 应用名称
        :param index: 窗口索引，默认为-1（最后一个窗口）
        :return: 窗口信息字典
        """
        info = self.get_windows_by_name(app_name)

        if info is None:
            return None

        if isinstance(info, dict):
            return info
        elif isinstance(info, list):
            if index < 0:
                index = len(info) + index
            if 0 <= index < len(info):
                return info[index]
        return None

    def _window_info(self):
        """
        获取当前鼠标位置的窗口信息
        :return: 窗口信息字典
        """
        # 获取鼠标位置
        point = wintypes.POINT()
        user32.GetCursorPos(ctypes.byref(point))

        # 获取鼠标位置的窗口
        hwnd = user32.WindowFromPoint(point)

        if not hwnd or not user32.IsWindow(hwnd):
            return None

        # 获取顶层窗口
        while True:
            parent = user32.GetParent(hwnd)
            if parent == 0 or parent == hwnd:
                break
            hwnd = parent

        return self.get_window_info(hwnd)


if __name__ == "__main__":
    # 测试代码
    wwininfo = WindowsWindowInfo()
    print("所有窗口信息:")
    windows = wwininfo.window_info()
    for name, info in windows.items():
        print(f"\n应用: {name}")
        if isinstance(info, dict):
            print(f"  位置: {info['location']}")
            print(f"  标题: {info['title']}")
        elif isinstance(info, list):
            for i, window_info in enumerate(info):
                print(f"  窗口 {i + 1}:")
                print(f"    位置: {window_info['location']}")
                print(f"    标题: {window_info['title']}")
