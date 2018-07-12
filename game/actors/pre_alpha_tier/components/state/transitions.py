from api.sax_engine.core.systems.state.transition import Transition
from api.sax_engine.events.event import Event
from ...pre_alpha_tier import PreAlphaTier
from ...event_id import EventId
from ...state_id import StateId
from typing import *


def transition__on_ground(actor: PreAlphaTier) -> Transition:
    target_state = StateId.on_ground

    subscriptions = [
        EventId.touch_floor
    ]

    def t_filter(event: Event) -> bool:
        return event.time == actor.get_scene_time()

    def t_check(events: Sequence[Event]) -> bool:
        return bool(events)

    return Transition(actor.event_stream, t_filter, t_check, target_state, *subscriptions)


def transition__in_air(actor: PreAlphaTier) -> Transition:
    target_state = StateId.in_air

    subscriptions = [
        EventId.touch_floor
    ]

    def t_filter(event: Event) -> bool:
        return event.time == actor.get_scene_time()

    def t_check(events: Sequence[Event]) -> bool:
        return not bool(events)

    return Transition(actor.event_stream, t_filter, t_check, target_state, *subscriptions)


def transition__panic(actor: PreAlphaTier, leave: bool=False) -> Transition:
    if leave:
        target_state = StateId.on_ground
    else:
        target_state = StateId.panic

    subscriptions = [
        EventId.worlds_of_pain
    ]
    if leave:
        def t_filter(event: Event) -> bool:
            return actor.get_scene_time() - event.time <= 7
    else:
        def t_filter(event: Event) -> bool:
            return event.time == actor.get_scene_time()

    if leave:
        # if inputs empty
        def t_check(events: Sequence[Event]) -> bool:
            return not bool(events)
    else:
        def t_check(events: Sequence[Event]) -> bool:
            return bool(events)

    return Transition(actor.event_stream, t_filter, t_check, target_state, *subscriptions)


def transition__watch_out(actor: PreAlphaTier, leave: bool=False) -> Transition:
    if leave:
        target_state = StateId.on_ground
    else:
        target_state = StateId.watch_out

    subscriptions = [
        EventId.watch_out,
        EventId.touch_wall
    ]

    if leave:
        def t_filter(event: Event) -> bool:
            return actor.get_scene_time() - event.time <= 3
    else:
        def t_filter(event: Event) -> bool:
            return event.time == actor.get_scene_time()

    if leave:
        # if inputs empty
        def t_check(events: Sequence[Event]) -> bool:
            return not bool(events)
    else:
        def t_check(events: Sequence[Event]) -> bool:
            return bool(events)

    return Transition(actor.event_stream, t_filter, t_check, target_state, *subscriptions)