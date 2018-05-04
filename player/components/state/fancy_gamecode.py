from api.sax_engine.vector import *
from .transitions import *

__all__ = [
    'movement_boilerplate', 'aiming_boilerplate',

    'halt_movement'
]


def movement_boilerplate(player: Player):
    # ! reference from previous version !
    # ===================================
    # if stick_input.x != 0:
    #     self.look_direction.y = 0
    #     if stick_input.x > 0:
    #         self.look_direction.x = 1
    #     else:
    #         self.look_direction.x = -1
    #     self.velocity.x = stick_input.length() * self.look_direction.x * const_RUN
    #     if abs(self.velocity.x) > 0 and self.state in [STAND, STAND_LEDGE]:
    #         self.events.append("run")
    # else:
    #     self.velocity.x = 0
    # ===================================
    #
    velocity = player.physics_data.velocity
    move = player.input_data.player_directional

    if move and move.x != 0:
        l_dir = +1 if move.x > 0 else -1
        player.shared_data.look_direction = Vector2(l_dir, 0)

        translation = l_dir * move.magnitude * player.physics_data.TRANSLATION_SPEED
        player.physics_data.velocity = Vector2(translation, velocity.y)
    else:
        halt_movement(player, halt_h=True)


def aiming_boilerplate(player: Player):
    directional = player.input_data.player_directional
    if directional.magnitude > 0:
        player.shared_data.look_direction = v_norm((directional.x, directional.y))
        return


def halt_movement(player: Player, halt_h: bool=False, halt_v: bool=False):
    vx, vy = player.physics_data.velocity
    if halt_h:
        vx = 0
    if halt_v:
        vy = 0
    player.physics_data.velocity = Vector2(vx, vy)
