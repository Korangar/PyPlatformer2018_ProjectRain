from api.sax_engine.vector import *
from .transitions import *

__all__ = [
    'movement_boilerplate',

    'halt_movement', 'invert_movement', 'invert_lookdir'
]


def movement_boilerplate(actor: PreAlphaTier, speed: float):
    velocity = actor.physics_data.velocity
    translation = actor.shared_data.look_direction.x * speed
    actor.physics_data.velocity = Vector2(translation, velocity.y)


def halt_movement(actor: PreAlphaTier, halt_h: bool=False, halt_v: bool=False):
    vx, vy = actor.physics_data.velocity
    if halt_h:
        vx = 0
    if halt_v:
        vy = 0
    actor.physics_data.velocity = Vector2(vx, vy)


def invert_movement(actor: PreAlphaTier, invert_h: bool=False, invert_v: bool=False):
    vx, vy = actor.physics_data.velocity
    if invert_h:
        vx = -vx
    if invert_v:
        vy = -vy
    actor.physics_data.velocity = Vector2(vx, vy)


def invert_lookdir(actor: PreAlphaTier):
    lx, ly = actor.shared_data.look_direction
    actor.shared_data.look_direction = Vector2(-lx, -ly)
