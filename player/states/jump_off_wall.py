from api.state.state import State
from ..player import Player
from . import PlayerStates, state_factory
from ._reusable_transitions import \
    transition__on_ground, \
    transition__in_air


@state_factory
def get_state__on_ground(player: Player):
    state = PlayerStates.jump_off_wall
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
            from api.utilities.geometry import Point
            if player.physics_data.absorb.x < 0:
                p = player.position
            else:
                x, y = player.position
                p = Point(x + player.physics_data.size, y)
            add_content_to_scene(player.scene, PointMarker(p, (255, 0, 0)))

    state.on_update += on_enter

    # return assembled state
    return state

