from api.events.event_stream import EventStream, Event
from api.scene.content import Actor
from api.state.machine import StateMachine
from api.utilities.geometry import Point
from api.utilities.vector import *

from enum import Enum
from typing import *


class PlayerEvents(Enum):
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


class PhysicsData:
    TRANSLATION_SPEED = 1.0
    JUMP_VELOCITY = 10.0
    JUMP_OFF_WALL_VELOCITY = 10.0
    GRAVITY_MODIFIER = 1.0

    def __init__(self):
        self.velocity = Vector2(0, 0)
        self.absorb = Vector2(0, 0)
        self.move_translation = 0
        self.size = Vector2(1, 1)


class InputData:
    def __init__(self):
        self.move = Vector2(0, 0)


class StateData:
    MAX_JUMPS = 1

    def __init__(self):
        self.jumps_left = 0
        self.look_direction = Vector2(0, 0)


class GraphicsData:
    def __init__(self):
        pass


class Player(Actor):
    def __init__(self, position=Point(0, 0)):
        super().__init__(position)
        # data
        self.physics_data = PhysicsData()
        self.input_data = InputData()
        self.state_data = StateData()
        self.graphics_data = GraphicsData()
        # state
        from .states import get_state_machine
        self.state_machine = get_state_machine(self)
        # events
        self.event_stream = EventStream()

    def push_event(self, event: PlayerEvents, **kwargs):
        self.event_stream.push(Event(event.name, self.scene.current_time, kwargs))

    def spawn(self):
        self.push_event(PlayerEvents.spawn)
        from .states import PlayerStates
        self.state_machine.set_state(PlayerStates.in_air)

    def update(self):
        self.state_machine.update()
        pass
