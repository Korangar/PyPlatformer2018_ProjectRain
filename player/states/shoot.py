from api.state.state import State
from ..player import Player
from . import PlayerStates, state_factory
from ._reusable_transitions import \
    transition__in_air, \
    transition__on_ground


@state_factory
def get_state__jump(player: Player):
    state = PlayerStates.shoot
    transitions = (
        transition__on_ground(player),
        transition__in_air(player)
    )

    # create state
    state = State(state, transitions)

    # create actions
    def on_enter(id_: PlayerStates):
        from api.utilities.vector import Vector2
        x, _ = player.physics_data.velocity
        player.physics_data.velocity = Vector2(x, player.physics_data.JUMP_VELOCITY)
        player.state_data.jumps_left -= 1

        if id_ == PlayerStates.on_ground:
            from api.scene import add_content_to_scene
            from api.prefab.debug.point_marker import PointMarker
            add_content_to_scene(player.scene, PointMarker(player.position, (255, 0, 0)))

    state.on_enter += on_enter

    # return assembled state
    return state
