from api.sax_engine.events.event_delegate import EventDelegate
from .transition import Transition, StateIdType
from typing import *


class State(Generic[StateIdType]):
    def __init__(self, id_: StateIdType, transitions: Sequence[Transition]):
        self.id = id_
        self.transitions = transitions
        self.on_enter: EventDelegate[StateIdType] = EventDelegate("State: {} entered!".format(str(self.id)))
        self.on_update: EventDelegate[StateIdType] = EventDelegate("State: {} updated!".format(str(self.id)))
        self.on_exit: EventDelegate[StateIdType] = EventDelegate("State: {} exited!".format(str(self.id)))

    def update(self) -> Optional[StateIdType]:
        active_transition = (result for result in (t() for t in self.transitions) if result)
        state_change = next(active_transition, None)
        self.on_update(state_change)
        # return state change
        return state_change
