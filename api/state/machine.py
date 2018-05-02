from ..events.event_delegate import EventDelegate
from .state import State, StateIdType
from typing import *


class StateMachine(Generic[StateIdType]):
    def __init__(self, *states: State[StateIdType]):
        self.state_dictionary: Dict[StateIdType, State[StateIdType]] = {s.id: s for s in states}
        self.on_state_change: EventDelegate[StateIdType] = EventDelegate("StateMachine: State changed!")
        self.current_state: State[StateIdType] = None

    def set_state(self, id_new: StateIdType):
        id_old = None
        if self.current_state:
            self.current_state.on_exit(id_new)
            id_old = self.current_state.id
        self.current_state = self.state_dictionary[id_new]
        self.current_state.on_enter(id_old)

    def update(self):
        new_state = self.current_state.update()
        if new_state:
            self.current_state = self.state_dictionary.get(new_state)
