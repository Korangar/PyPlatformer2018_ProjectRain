from api.state.transition import Transition
from api.events.event import Event
from ..player import Player, PlayerEvents
from . import PlayerStates
from typing import *


def transition__on_ground(player: Player) -> Transition:
    target_state = PlayerStates.on_ground

    subscriptions = [
        PlayerEvents.touch_floor
    ]

    def t_filter(event: Event) -> bool:
        return event.time == player.get_scene_time()

    def t_check(events: Sequence[Event]) -> bool:
        return bool(events)

    return Transition(player.event_stream, t_filter, t_check, target_state, *subscriptions)


def transition__in_air(player: Player) -> Transition:
    target_state = PlayerStates.in_air

    subscriptions = [
        PlayerEvents.touch_floor
    ]

    def t_filter(event: Event) -> bool:
        return event.time == player.get_scene_time()

    def t_check(events: Sequence[Event]) -> bool:
        return not bool(events)

    return Transition(player.event_stream, t_filter, t_check, target_state, *subscriptions)


def transition__aiming(player: Player, enable=True) -> Transition:
    target_state = PlayerStates.aiming
    subscriptions = [
        PlayerEvents.press_take_aim
    ]

    def t_filter(event: Event) -> bool:
        return event.time == player.get_scene_time()

    if enable:
        def t_check(events: Sequence[Event]) -> bool:
            return bool(events)
    else:
        def t_check(events: Sequence[Event]) -> bool:
            return not bool(events)

    return Transition(player.event_stream, t_filter, t_check, target_state, *subscriptions)


def transition__shoot(player: Player) -> Transition:
    target_state = PlayerStates.shoot
    subscriptions = [
        PlayerEvents.press_shoot
    ]

    def t_filter(event: Event) -> bool:
        return event.time == player.get_scene_time()

    def t_check(events: Sequence[Event]) -> bool:
        return bool(events)

    return Transition(player.event_stream, t_filter, t_check, target_state, *subscriptions)


def transition__jump(player: Player) -> Transition:
    target_state = PlayerStates.jump
    subscriptions = [
        PlayerEvents.press_jump
    ]

    def t_filter(event: Event) -> bool:
        return event.time == player.get_scene_time()

    def t_check(events: Sequence[Event]) -> bool:
        return player.state_data.jumps_left > 0 and bool(events)

    return Transition(player.event_stream, t_filter, t_check, target_state, *subscriptions)
