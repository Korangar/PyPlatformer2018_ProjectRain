from api.sax_engine.core.systems.state.transition import Transition
from api.sax_engine.events.event import Event
from player.player import Player
from player.event_id import PlayerEventId
from player.state_id import StateId
from typing import *


def transition__on_ground(player: Player) -> Transition:
    target_state = StateId.on_ground

    subscriptions = [
        PlayerEventId.touch_floor
    ]

    def t_filter(event: Event) -> bool:
        return event.time == player.get_scene_time()

    def t_check(events: Sequence[Event]) -> bool:
        return bool(events)

    return Transition(player.event_stream, t_filter, t_check, target_state, *subscriptions)


def transition__in_air(player: Player) -> Transition:
    target_state = StateId.in_air

    subscriptions = [
        PlayerEventId.touch_floor
    ]

    def t_filter(event: Event) -> bool:
        return event.time == player.get_scene_time()

    def t_check(events: Sequence[Event]) -> bool:
        return not bool(events)

    return Transition(player.event_stream, t_filter, t_check, target_state, *subscriptions)


def transition__aiming(player: Player, enable=True, return_to=None) -> Transition:
    if enable:
        target_state = StateId.aiming
        subscriptions = [
            PlayerEventId.press_take_aim
        ]
    else:
        assert return_to
        target_state = return_to
        subscriptions = [
            PlayerEventId.release_take_aim
        ]

    def t_filter(event: Event) -> bool:
        return event.time == player.get_scene_time()

    if enable:
        def t_check(events: Sequence[Event]) -> bool:
            return bool(events) or player.input_data.gamepad.input_state.trigger_r > 0.5
    else:
        def t_check(events: Sequence[Event]) -> bool:
            return bool(events)

    return Transition(player.event_stream, t_filter, t_check, target_state, *subscriptions)


def transition__shoot(player: Player) -> Transition:
    target_state = StateId.shoot
    subscriptions = [
        PlayerEventId.press_shoot
    ]

    def t_filter(event: Event) -> bool:
        return event.time == player.get_scene_time()

    def t_check(events: Sequence[Event]) -> bool:
        return bool(events)

    return Transition(player.event_stream, t_filter, t_check, target_state, *subscriptions)


def transition__jump(player: Player) -> Transition:
    target_state = StateId.jump
    subscriptions = [
        PlayerEventId.press_jump
    ]

    def t_filter(event: Event) -> bool:
        return event.time == player.get_scene_time()

    def t_check(events: Sequence[Event]) -> bool:
        return player.shared_data.jumps_left > 0 and bool(events)

    return Transition(player.event_stream, t_filter, t_check, target_state, *subscriptions)


def transition__jump_off_wall(player: Player) -> Transition:
    target_state = StateId.jump_off_wall
    subscriptions = [
        PlayerEventId.press_jump,
        PlayerEventId.touch_wall
    ]

    def t_filter(event: Event) -> bool:
        return event.time == player.get_scene_time()

    def t_check(events: Sequence[Event]) -> bool:
        return any(e == PlayerEventId.touch_wall for e in events) and \
               any(e == PlayerEventId.press_jump for e in events)

    return Transition(player.event_stream, t_filter, t_check, target_state, *subscriptions)
