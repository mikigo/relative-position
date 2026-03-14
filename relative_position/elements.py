#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
元素定义模块
提供 Ele 类用于定义UI元素的相对位置
"""

from typing import List, Tuple, Optional


class Ele:
    """
    元素类 - 用于定义UI元素的相对位置和方向

    使用示例：
    ```python
    close_button = Ele(
        direction="left_bottom",
        location=[20, 20, 50, 35]
    )
    ```
    """

    # 定义有效的方向
    VALID_DIRECTIONS = (
        "left_bottom",
        "left_top",
        "right_top",
        "right_bottom",
        "top_center",
        "bottom_center",
        "left_center",
        "right_center",
        "window_size",
    )

    def __init__(self, direction: str, location: List[int]):
        """
        初始化元素

        :param direction: 参考点方向
            可选值: left_bottom, left_top, right_top, right_bottom,
                     top_center, bottom_center, left_center, right_center, window_size
        :param location: 相对位置坐标 [x, y, width, height]
        """
        if direction not in self.VALID_DIRECTIONS:
            raise ValueError(
                f"无效的方向: {direction}. "
                f"有效值为: {', '.join(self.VALID_DIRECTIONS)}"
            )

        if not isinstance(location, (list, tuple)) or len(location) != 4:
            raise ValueError(
                f"location 必须是包含4个元素的列表或元组: [x, y, width, height]"
            )

        if not all(isinstance(val, (int, float)) for val in location):
            raise ValueError(
                f"location 中的所有元素必须是数字: {location}"
            )

        self.direction = direction
        self.location = location

    def __repr__(self) -> str:
        """返回元素的字符串表示"""
        return f"Ele(direction={self.direction!r}, location={self.location!r})"

    def __str__(self) -> str:
        """返回元素的字符串表示"""
        return self.__repr__()

    def get_position(self) -> Tuple[str, List[int]]:
        """
        获取元素的位置信息

        :return: (direction, location) 元组
        """
        return self.direction, self.location

    def to_dict(self) -> dict:
        """
        将元素转换为字典

        :return: 包含 direction 和 location 的字典
        """
        return {
            "direction": self.direction,
            "location": self.location
        }

    @property
    def x(self) -> int:
        """获取 x 坐标"""
        return int(self.location[0])

    @property
    def y(self) -> int:
        """获取 y 坐标"""
        return int(self.location[1])

    @property
    def width(self) -> int:
        """获取宽度"""
        return int(self.location[2])

    @property
    def height(self) -> int:
        """获取高度"""
        return int(self.location[3])


class Elements:
    """
    元素集合类 - 用于管理多个元素定义

    使用示例：
    ```python
    elements = Elements()
    elements.add("close_button", Ele(direction="left_bottom", location=[20, 20, 50, 35]))
    elements.add("open_button", Ele(direction="right_top", location=[10, 10, 40, 30]))

    # 或者使用字典初始化
    elements = Elements({
        "close_button": Ele(direction="left_bottom", location=[20, 20, 50, 35]),
        "open_button": Ele(direction="right_top", location=[10, 10, 40, 30])
    })
    ```
    """

    def __init__(self, elements: Optional[dict] = None):
        """
        初始化元素集合

        :param elements: 初始元素字典 {name: Ele}
        """
        self._elements = {}
        if elements:
            for name, ele in elements.items():
                self.add(name, ele)

    def add(self, name: str, element: Ele):
        """
        添加元素

        :param name: 元素名称
        :param element: 元素对象
        """
        if not isinstance(element, Ele):
            raise TypeError(f"元素必须是 Ele 类的实例，得到的是: {type(element)}")
        self._elements[name] = element

    def get(self, name: str) -> Optional[Ele]:
        """
        获取元素

        :param name: 元素名称
        :return: 元素对象，如果不存在返回 None
        """
        return self._elements.get(name)

    def remove(self, name: str):
        """
        移除元素

        :param name: 元素名称
        """
        if name in self._elements:
            del self._elements[name]

    def list_names(self) -> List[str]:
        """
        获取所有元素名称

        :return: 元素名称列表
        """
        return list(self._elements.keys())

    def to_dict(self) -> dict:
        """
        将元素集合转换为字典

        :return: {name: {direction, location}} 字典
        """
        return {
            name: ele.to_dict()
            for name, ele in self._elements.items()
        }

    def __getitem__(self, name: str) -> Ele:
        """
        通过名称获取元素

        :param name: 元素名称
        :return: 元素对象
        :raises KeyError: 如果元素不存在
        """
        if name not in self._elements:
            raise KeyError(f"元素 '{name}' 不存在")
        return self._elements[name]

    def __setitem__(self, name: str, element: Ele):
        """
        通过名称设置元素

        :param name: 元素名称
        :param element: 元素对象
        """
        self.add(name, element)

    def __delitem__(self, name: str):
        """
        通过名称删除元素

        :param name: 元素名称
        :raises KeyError: 如果元素不存在
        """
        if name not in self._elements:
            raise KeyError(f"元素 '{name}' 不存在")
        self.remove(name)

    def __contains__(self, name: str) -> bool:
        """
        检查元素是否存在

        :param name: 元素名称
        :return: True 如果存在，否则 False
        """
        return name in self._elements

    def __len__(self) -> int:
        """
        获取元素数量

        :return: 元素数量
        """
        return len(self._elements)

    def __iter__(self):
        """
        迭代元素

        :return: 元素名称的迭代器
        """
        return iter(self._elements)

    def __repr__(self) -> str:
        """返回元素集合的字符串表示"""
        return f"Elements({self._elements!r})"
