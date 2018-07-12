from api.sax_engine.vector import Vector2
from api.sax_engine.core.systems.state.state import State
from .transitions import *
from .fancy_gamecode import *

__all__ = ['create_states']

STATE_FACTORIES = []


def create_states(actor):
    return (f(actor) for f in STATE_FACTORIES)


def state_factory(d):
    print("Player state '{}' loaded.".format(d.__name__))
    STATE_FACTORIES.append(d)
    return d


@state_factory
def get_state__in_air(actor: PreAlphaTier):
    state = StateId.in_air
    transitions = (
        transition__panic(actor),
        transition__on_ground(actor),
    )
    # todo enable aiming in mid air

    # create state
    state = State(state, transitions)

    # create actions
    def on_enter(id_: StateId):
        halt_movement(actor, halt_h=True)

    def on_update(id_: StateId):
        pass

    def on_exit(id_: StateId):
        pass

    state.on_enter += on_enter
    state.on_update += on_update
    state.on_exit += on_exit

    # return assembled state
    return state


@state_factory
def get_state__on_ground(actor: PreAlphaTier):
    state = StateId.on_ground
    transitions = (
        transition__panic(actor),
        transition__in_air(actor),
        transition__watch_out(actor)
    )

    # create state
    state = State(state, transitions)

    # create actions
    def on_enter(id_: StateId):
        pass

    def on_update(id_: StateId):
        movement_boilerplate(actor, actor.physics_data.TRANSLATION_SPEED * 0.5)

    def on_exit(id_: StateId):
        pass

    state.on_enter += on_enter
    state.on_update += on_update
    state.on_exit += on_exit

    # return assembled state
    return state


@state_factory
def get_state__watch_out(actor: PreAlphaTier):
    state = StateId.watch_out
    transitions = (
        transition__panic(actor),
        transition__watch_out(actor, leave=True),
    )

    # create state
    state = State(state, transitions)

    # create actions
    def on_enter(id_: StateId):
        actor.physics_data.size = Vector2(0.5, 1.2)
        halt_movement(actor, halt_h=True)

    def on_update(id_: StateId):
        # todo look around or sth
        pass

    def on_exit(id_: StateId):
        actor.physics_data.size = Vector2(1.2, 0.6)
        invert_lookdir(actor)

    state.on_enter += on_enter
    state.on_update += on_update
    state.on_exit += on_exit

    # return assembled state
    return state


@state_factory
def get_state__panic(actor: PreAlphaTier):
    state = StateId.panic
    transitions = [
        transition__panic(actor),
        transition__panic(actor, leave=True)
    ]

    # create state
    state = State(state, transitions)

    # create actions
    def on_enter(id_: StateId):
        if id_ == StateId.panic:
            invert_movement(actor, invert_h=True)

    def on_update(id_: StateId):
        movement_boilerplate(actor, actor.physics_data.TRANSLATION_SPEED*1.5)

    def on_exit(id_: StateId):
        actor.push_event(EventId.watch_out)
        halt_movement(actor, halt_h=True)

    state.on_enter += on_enter
    state.on_update += on_update
    state.on_exit += on_exit

    # return assembled state
    return state
