from api.state.state import State
from ..player import Player
from . import PlayerStates, state_factory
from ._reusable_transitions import \
    transition__shoot, \
    transition__jump, \
    transition__in_air, \
    transition__aiming


@state_factory
def get_state__on_ground(player: Player):
    state = PlayerStates.on_ground
    transitions = (
        transition__in_air(player),
        transition__shoot(player),
        transition__aiming(player),
        transition__jump(player)
    )

    # create state
    state = State(state, transitions)

    # create actions
    def on_update(id_: PlayerStates):
        if player.input_data.move.x:
            from api.utilities.vector import Vector2, v_norm
            translation = player.input_data.move.x * player.physics_data.TRANSLATION_SPEED
            player.physics_data.velocity = Vector2(translation, player.physics_data.velocity.y)
            player.state_data.look_direction = Vector2(*v_norm((player.input_data.move.x, 0)))

    state.on_update += on_update

    # return assembled state
    return state

