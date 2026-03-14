#!/usr/bin/env python3
# _*_ coding:utf-8 _*_


class ApplicationStartError(Exception):
    """
    应用程序未启动
    """

    def __init__(self, result):
        """
        应用程序未启动
        :param result: 结果
        """
        err = f"应用程序未启动,{result}"
        super().__init__(err)


class ApplicationError(Exception):
    """应用程序错误"""

    def __init__(self, msg):
        """
        应用程序错误
        :param msg: 结果
        """
        super().__init__(msg)


class GetWindowInformation(Exception):
    """获取窗口信息错误"""

    def __init__(self, msg):
        """
        获取窗口信息错误
        :param msg: 结果
        """
        super().__init__(msg)


class NoSetReferencePoint(Exception):
    """未设置参考点错误"""

    def __init__(self, msg):
        """
        未设置参考点错误
        :param msg: 结果
        """
        super().__init__(msg)