from api.state.transition import Transition
from api.state.state import State
from api.events.event import Event

from ..player import Player, PlayerEvents
from . import PlayerStates, state_factory
from ._reusable_transitions import \
    transition__shoot, \
    transition__aiming, \
    transition__on_ground, \
    transition__jump

from typing import *


@state_factory
def get_state__in_air(player: Player):
    state = PlayerStates.in_air
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
    def on_update(id_: PlayerStates):
        if player.input_data.move.x:
            from api.utilities.vector import Vector2, v_norm
            translation = player.input_data.move.x * player.physics_data.TRANSLATION_SPEED
            player.physics_data.velocity = Vector2(translation, player.physics_data.velocity.y)
            player.state_data.look_direction = Vector2(*v_norm((player.input_data.move.x, 0)))

    state.on_update += on_update

    # return assembled state
    return state


def transition__jump_off_wall(player: Player) -> Transition:
    target_state = PlayerStates.jump_off_wall
    subscriptions = [
        PlayerEvents.press_jump,
        PlayerEvents.touch_wall
    ]

    def t_filter(event: Event) -> bool:
        return event.time == player.get_scene_time()

    def t_check(events: Sequence[Event]) -> bool:
        return any(e == PlayerEvents.touch_wall for e in events) and \
               any(e == PlayerEvents.press_jump for e in events)

    return Transition(player.event_stream, t_filter, t_check, target_state, *subscriptions)
