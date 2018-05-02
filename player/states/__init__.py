from . import *

from api.state.machine import StateMachine

import enum


class PlayerStates(enum.Enum):
    in_air = 0
    on_ground = 1
    aiming = 2

    shoot = 10
    jump = 11
    jump_off_wall = 12


ALL_STATES = []


def state_factory(func):
    ALL_STATES.append(func)
    return func


def get_state_machine(player) -> StateMachine:
    return StateMachine(*(factory(player) for factory in ALL_STATES))
