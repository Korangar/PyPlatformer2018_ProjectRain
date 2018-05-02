from ..events.event_stream import EventStream
from ..events.event import Event, EventIdType
from typing import *

StateIdType = TypeVar("_StateType")


class Transition(Generic[StateIdType]):
    def __init__(self,
                 event_stream: EventStream,
                 f: Callable[[Event], bool],
                 c: Callable[[(Sequence[Event])], bool],
                 state: StateIdType,
                 subscriptions: EventIdType):
        self.next_state = state
        self.filter_input = f
        self.check = c
        self.input: List[Event] = []
        event_stream.subscribe(self.add_input, subscriptions)

    def add_input(self, input_: Event):
        self.input.append(input_)
        self.input = list(filter(self.filter_input, self.input))

    def __call__(self) -> Optional[StateIdType]:
        state_change = None
        self.input = list(filter(self.filter_input, self.input))
        if self.check(self.input):
            self.input.clear()
            state_change = self.next_state
        return state_change
