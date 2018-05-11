from api.sax_engine.core.systems.state.state import State
from player.components.state.transitions import *
from .fancy_gamecode import *

__all__ = ['create_states']

STATE_FACTORIES = []


def create_states(player):
    return (f(player) for f in STATE_FACTORIES)


def state_factory(d):
    print("Player state '{}' loaded.".format(d.__name__))
    STATE_FACTORIES.append(d)
    return d


@state_factory
def get_state__in_air(player: Player):
    state = StateId.in_air
    transitions = (
        transition__on_ground(player),
        # transition__aiming(player),
        transition__shoot(player),
        transition__jump_off_wall(player),
        transition__jump(player)
    )
    # todo enable aiming in mid air

    # create state
    state = State(state, transitions)

    # create actions
    def on_enter(id_: StateId):
        pass

    def on_update(id_: StateId):
        movement_boilerplate(player)

    def on_exit(id_: StateId):
        halt_movement(player, halt_h=True)

    state.on_enter += on_enter
    state.on_update += on_update
    state.on_exit += on_exit

    # return assembled state
    return state


@state_factory
def get_state__on_ground(player: Player):
    state = StateId.on_ground
    transitions = (
        transition__in_air(player),
        transition__shoot(player),
        transition__aiming(player),
        transition__jump(player)
    )

    # create state
    state = State(state, transitions)

    # create actions
    def on_enter(id_: StateId):
        player.shared_data.jumps_left = player.shared_data.MAX_JUMPS

    def on_update(id_: StateId):
        movement_boilerplate(player)

    def on_exit(id_: StateId):
        halt_movement(player, halt_h=True)

    state.on_enter += on_enter
    state.on_update += on_update
    state.on_exit += on_exit

    # return assembled state
    return state


@state_factory
def get_state__aiming(player: Player):
    state = StateId.aiming
    transitions = (
        transition__aiming(player, enable=False, return_to=StateId.on_ground),
        transition__shoot(player)
    )
    # todo fck that aiming in air needs own state
    # todo make special handling for hitting the ground while aiming in midair

    # create state
    state = State(state, transitions)

    # create actions
    def on_update(id_: StateId):
        aiming_boilerplate(player)

    # todo if in air slow the time on enter, restore on exit
    state.on_update += on_update

    # return assembled state
    return state


@state_factory
def get_state__shoot(player: Player):
    state = StateId.shoot
    transitions = (
        transition__aiming(player, enable=True),
        transition__on_ground(player),
        transition__in_air(player)
    )

    # create state
    state = State(state, transitions)

    # create actions
    def on_enter(id_: StateId):
        shooting_boilerplate(player)

    state.on_enter += on_enter

    # return assembled state
    return state


@state_factory
def get_state__jump(player: Player):
    state = StateId.jump
    transitions = (
        transition__on_ground(player),
        transition__in_air(player)
    )

    # create state
    state = State(state, transitions)

    # create actions
    def on_enter(id_: StateId):
        from api.sax_engine.vector import Vector2
        x, _ = player.physics_data.velocity
        player.physics_data.velocity = Vector2(x, player.physics_data.JUMP_VELOCITY)
        player.shared_data.jumps_left -= 1

        if id_ == StateId.on_ground:
            from api.sax_engine.core import add_content_to_scene
            from prefabs.debug import PointMarker
            add_content_to_scene(player.scene, PointMarker(player.position, (255, 0, 0)))

    state.on_enter += on_enter

    # return assembled state
    return state


@state_factory
def get_state__jump_of_wall(player: Player):
    state = StateId.jump_off_wall
    transitions = (
        transition__on_ground(player),
        transition__in_air(player)
    )

    # create state
    state = State(state, transitions)

    # create actions
    def on_enter(id_: StateId):
        from api.sax_engine.vector import Vector2
        x, _ = player.physics_data.velocity
        player.physics_data.velocity = Vector2(x, player.physics_data.JUMP_VELOCITY)
        player.shared_data.jumps_left -= 1

        if id_ == StateId.on_ground:
            from api.sax_engine.core import add_content_to_scene
            from prefabs.debug import PointMarker
            from api.sax_engine.geometry import Point
            if player.physics_data.absorb.x < 0:
                p = player.position
            else:
                x, y = player.position
                p = Point(x + player.physics_data.size, y)
            add_content_to_scene(player.scene, PointMarker(p, (255, 0, 0), 5))

    state.on_update += on_enter

    # return assembled state
    return state
