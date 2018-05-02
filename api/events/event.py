from typing import *


EventIdType = str


class Event(NamedTuple):
    id: EventIdType
    time: float
    kwargs: Dict = {}
