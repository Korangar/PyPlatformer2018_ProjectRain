from api.state.state import State
from ..player import Player
from . import PlayerStates, state_factory
from ._reusable_transitions import \
    transition__shoot, \
    transition__aiming


@state_factory
def get_state__aiming(player: Player):
    # assemble transitions
    transitions = (
        transition__aiming(player, enable=False),
        transition__shoot(player)
    )
    # todo make special handling for hitting the ground while aiming in midair

    # create state
    state = State(PlayerStates.in_air, transitions)

    # create actions
    def on_update(id_: PlayerStates):
        from api.utilities.vector import v_norm
        aim_direction = v_norm(player.input_data.move)
        player.state_data.look_direction = aim_direction

    # todo if in air slow the time on enter, restore on exit
    state.on_update += on_update

    # return assembled state
    return state

