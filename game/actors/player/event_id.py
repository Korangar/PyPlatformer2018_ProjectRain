from enum import Enum


class PlayerEventId(Enum):
    actor_spawn = 0
    actor_destroy = 1

    touch_wall = 10
    touch_floor = 11
    touch_ceiling = 12

    press_jump = 50
    press_shoot = 51
    press_take_aim = 52

    release_jump = 60
    release_shoot = 61
    release_take_aim = 62
