#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
元素定义模块
提供 Ele 类用于定义UI元素的相对位置
"""

from typing import List, Tuple, Optional, Union, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from relative_position.app import App


class Direction(Enum):
    """
    方向枚举，定义元素相对于窗口的参考点方向

    角点参考:
    - LEFT_TOP: 左上角
    - RIGHT_TOP: 右上角
    - LEFT_BOTTOM: 左下角
    - RIGHT_BOTTOM: 右下角

    边界中心参考:
    - TOP_CENTER: 上边界中心
    - BOTTOM_CENTER: 下边界中心
    - LEFT_CENTER: 左边界中心
    - RIGHT_CENTER: 右边界中心

    完整窗口:
    - WINDOW_SIZE: 整个窗口
    """
    LEFT_TOP = "left_top"
    RIGHT_TOP = "right_top"
    LEFT_BOTTOM = "left_bottom"
    RIGHT_BOTTOM = "right_bottom"
    TOP_CENTER = "top_center"
    BOTTOM_CENTER = "bottom_center"
    LEFT_CENTER = "left_center"
    RIGHT_CENTER = "right_center"
    WINDOW_SIZE = "window_size"


class Ele:
    """
    元素类 - 用于定义UI元素的相对位置和方向

    使用示例：
    ```python
    from relative_position import Ele, Direction

    # 使用 bbox 参数
    close_button = Ele(
        direction=Direction.LEFT_BOTTOM,
        bbox=[20, 20, 50, 35]
    )

    # 或者使用 center 参数
    close_button = Ele(
        direction=Direction.LEFT_BOTTOM,
        center=[30, 30]  # 相对 direction 的偏移坐标
    )

    # 或者使用字符串（向后兼容）
    close_button = Ele(
        direction="left_bottom",
        bbox=[20, 20, 50, 35]
    )
    ```
    """

    def __init__(
        self,
        direction: Union[Direction, str],
        bbox: Optional[List[int]] = None,
        center: Optional[List[int]] = None,
        app: Optional['App'] = None,
        name: Optional[str] = None
    ):
        """
        初始化元素

        :param direction: 参考点方向，可以使用 Direction 枚举或字符串
            枚举值: Direction.LEFT_BOTTOM, Direction.LEFT_TOP, Direction.RIGHT_TOP, Direction.RIGHT_BOTTOM,
                     Direction.TOP_CENTER, Direction.BOTTOM_CENTER, Direction.LEFT_CENTER, Direction.RIGHT_CENTER,
                     Direction.WINDOW_SIZE
            字符串值: "left_bottom", "left_top", "right_top", "right_bottom",
                      "top_center", "bottom_center", "left_center", "right_center", "window_size"
        :param bbox: 边界框坐标 [x, y, width, height]，与 center 参数二选一
        :param center: 相对 direction 的偏移坐标 [x, y]，与 bbox 参数二选一
        :param app: 可选的 App 实例，用于关联元素到应用
        :param name: 可选的元素名称，用于在 App 中注册
        """
        # 验证 bbox 和 center 必须提供一个，且不能同时提供
        if bbox is None and center is None:
            raise ValueError("必须提供 bbox 或 center 参数之一")
        if bbox is not None and center is not None:
            raise ValueError("bbox 和 center 参数不能同时提供，请选择其中一个")

        # 处理 direction 参数，支持枚举和字符串
        if isinstance(direction, str):
            # 字符串转枚举
            try:
                direction = Direction(direction)
            except ValueError:
                raise ValueError(
                    f"无效的方向: {direction}. "
                    f"有效值为: {', '.join([d.value for d in Direction])}"
                )
        elif not isinstance(direction, Direction):
            raise TypeError(
                f"direction 必须是 Direction 枚举或字符串类型，得到的是: {type(direction)}"
            )

        # 验证 bbox 参数
        if bbox is not None:
            if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
                raise ValueError(
                    f"bbox 必须是包含4个元素的列表或元组: [x, y, width, height]"
                )
            if not all(isinstance(val, (int, float)) for val in bbox):
                raise ValueError(
                    f"bbox 中的所有元素必须是数字: {bbox}"
                )

        # 验证 center 参数
        if center is not None:
            if not isinstance(center, (list, tuple)) or len(center) != 2:
                raise ValueError(
                    f"center 必须是包含2个元素的列表或元组: [x, y]"
                )
            if not all(isinstance(val, (int, float)) for val in center):
                raise ValueError(
                    f"center 中的所有元素必须是数字: {center}"
                )

        self.direction = direction
        self._bbox = bbox
        self._center = center
        self._app = app
        self._name = name

        # 如果提供了 App 实例，自动注册元素
        if self._app is not None:
            if self._name is None:
                self._name = self._app.register_element(self)
            else:
                self._app.add_element(self._name, self)

    def __repr__(self) -> str:
        """返回元素的字符串表示"""
        if self._bbox is not None:
            return f"Ele(direction={self.direction!r}, bbox={self._bbox!r})"
        else:
            return f"Ele(direction={self.direction!r}, center={self._center!r})"

    def __str__(self) -> str:
        """返回元素的字符串表示"""
        return self.__repr__()

    def get_position(self) -> Tuple[str, Optional[List[int]], Optional[List[int]]]:
        """
        获取元素的位置信息

        :return: (direction, bbox, center) 元组
        """
        return self.direction, self._bbox, self._center

    def to_dict(self) -> dict:
        """
        将元素转换为字典

        :return: 包含 direction 和 bbox 或 center 的字典
        """
        result = {
            "direction": self.direction.value if isinstance(self.direction, Direction) else self.direction
        }
        if self._bbox is not None:
            result["bbox"] = self._bbox
        if self._center is not None:
            result["center"] = self._center
        return result

    @property
    def bbox(self) -> Optional[List[int]]:
        """获取边界框"""
        return self._bbox

    @property
    def center_offset(self) -> Optional[List[int]]:
        """获取中心偏移"""
        return self._center

    @property
    def x(self) -> Optional[int]:
        """获取 x 坐标（仅当使用 bbox 时可用）"""
        if self._bbox is None:
            raise AttributeError("x 属性仅在使用 bbox 参数时可用")
        return int(self._bbox[0])

    @property
    def y(self) -> Optional[int]:
        """获取 y 坐标（仅当使用 bbox 时可用）"""
        if self._bbox is None:
            raise AttributeError("y 属性仅在使用 bbox 参数时可用")
        return int(self._bbox[1])

    @property
    def width(self) -> Optional[int]:
        """获取宽度（仅当使用 bbox 时可用）"""
        if self._bbox is None:
            raise AttributeError("width 属性仅在使用 bbox 参数时可用")
        return int(self._bbox[2])

    @property
    def height(self) -> Optional[int]:
        """获取高度（仅当使用 bbox 时可用）"""
        if self._bbox is None:
            raise AttributeError("height 属性仅在使用 bbox 参数时可用")
        return int(self._bbox[3])

    def set_app(self, app: 'App', name: Optional[str] = None):
        """
        关联元素到 App 实例

        :param app: App 实例
        :param name: 元素名称，可选
        """
        self._app = app
        if name is not None:
            self._name = name
            self._app.add_element(self._name, self)
        elif self._name is None:
            self._name = self._app.register_element(self)
        else:
            self._app.add_element(self._name, self)

    def center(self) -> Tuple[float, float]:
        """
        获取元素的中心坐标

        :return: (x, y) 坐标
        :raises RuntimeError: 如果元素未关联到 App 实例
        """
        if self._app is None:
            raise RuntimeError("元素未关联到 App 实例，请先使用 set_app() 方法或在创建时提供 app 参数")

        if self._name is None:
            self._name = self._app.register_element(self)

        return self._app.get_center(self)

    def click(self, button: str = 'left'):
        """
        点击元素

        :param button: 按钮类型，'left', 'right', 'middle'，默认 'left'
        """
        from relative_position.app import Mouse

        x, y = self.center()
        Mouse.move_to(int(x), int(y))

        if button == 'left':
            Mouse.click(button='left', clicks=1)
        elif button == 'right':
            Mouse.click(button='right', clicks=1)
        elif button == 'middle':
            Mouse.click(button='middle', clicks=1)
        else:
            raise ValueError(f"不支持的按钮类型: {button}")

    def right_click(self):
        """右键点击元素"""
        self.click(button='right')

    def double_click(self, button: str = 'left'):
        """
        双击元素

        :param button: 按钮类型，默认 'left'
        """
        from relative_position.app import Mouse

        x, y = self.center()
        Mouse.move_to(int(x), int(y))
        Mouse.double_click(button=button)

    def hover(self):
        """鼠标悬停在元素上"""
        from relative_position.app import Mouse

        x, y = self.center()
        Mouse.move_to(int(x), int(y))


class Elements:
    """
    元素集合类 - 用于管理多个元素定义

    使用示例：
    ```python
    elements = Elements()
    elements.add("close_button", Ele(direction="left_bottom", bbox=[20, 20, 50, 35]))
    elements.add("open_button", Ele(direction="right_top", bbox=[10, 10, 40, 30]))

    # 或者使用 center 参数
    elements.add("cancel_button", Ele(direction="top_center", center=[100, 50]))

    # 或者使用字典初始化
    elements = Elements({
        "close_button": Ele(direction="left_bottom", bbox=[20, 20, 50, 35]),
        "open_button": Ele(direction="right_top", bbox=[10, 10, 40, 30])
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

        :return: {name: {direction, bbox}} 或 {name: {direction, center}} 字典
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
