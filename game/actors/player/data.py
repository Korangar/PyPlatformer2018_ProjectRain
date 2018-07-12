from api.sax_engine.vector import Vector2
from api.xinput import XInputGamepad, AnalogStick
from .state_id import *

__all__ = ["PhysicsData", "InputData", "SharedData", "GraphicsData"]


class PhysicsData:
    TRANSLATION_SPEED = 12.0
    JUMP_VELOCITY = 25.0
    JUMP_OFF_WALL_VELOCITY = 10.0
    GRAVITY_MODIFIER = 50.0

    def __init__(self):
        self.velocity = Vector2(0, 0)
        self.absorb = Vector2(0, 0)
        self.size = Vector2(1, 2)


class InputData:
    def __init__(self):
        self.gamepad: XInputGamepad = None
        # todo move this somewhere else
        # todo input system in general seems pointless rn
        self.player_directional: AnalogStick = None


class SharedData:
    DEFAULT_STATE = StateId.in_air
    MAX_JUMPS = 1

    def __init__(self):
        self.jumps_left = 0
        self.look_direction = Vector2(1, 0)


class GraphicsData:
    def __init__(self):
        pass