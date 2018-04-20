from typing import *

_State = TypeVar('_State')
_Input = TypeVar('_Input')
DeltaFunction = Mapping[Tuple[_State, _Input], _State]


class FSM(Generic[_State, _Input]):
    def __init__(self, default: _State, delta: DeltaFunction):
        self.default_state = default
        self.delta_function = delta

    def transition(self, state: _State, input_: _Input) -> _State:
        return self.delta_function.get((state, input_), state)


if __name__ == "__main__":
    from enum import Enum

    class E1(Enum):
        A = 1
        B = 2

    class E2(Enum):
        A = 1
        B = 2

    fsm1 = FSM(E1.A, {(E1.A, E2.A): E1.A})
    fsm1.transition(E1.A, E2.A)
