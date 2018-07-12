from enum import Enum


class EventId(Enum):
    actor_spawn = 0
    actor_destroy = 1

    touch_wall = 10
    touch_floor = 11
    touch_ceiling = 12

    watch_out = 30
    worlds_of_pain = 31
