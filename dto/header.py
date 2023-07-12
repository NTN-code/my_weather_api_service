from typing import NamedTuple


class Header(NamedTuple):
    minY: int
    maxY: int
    minX: int
    maxX: int
    dy: int
    dx: int
    multiplier: int
    empty_value: int