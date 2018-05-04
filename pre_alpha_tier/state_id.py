from enum import Enum

__all__ = ['StateId']


class StateId(Enum):
    in_air = 0
    on_ground = 1
    watch_out = 2
    panic = 3


