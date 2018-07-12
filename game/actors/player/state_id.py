from enum import Enum

__all__ = ['StateId']


class StateId(Enum):
    in_air = 0
    on_ground = 1
    aiming = 2

    shoot = 10
    jump = 11
    jump_off_wall = 12
