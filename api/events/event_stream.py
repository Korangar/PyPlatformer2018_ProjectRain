from .event import Event, EventIdType
from .event_delegate import EventDelegate, Action
from typing import *


class EventStream:
    def __init__(self):
        self.listeners: (Dict[EventIdType, EventDelegate[Event]]) = {}

    def push(self, event: Event) -> None:
        if event.id in self.listeners:
            self.listeners[event.id](event)

    def subscribe(self, action: Action[Event], *subscriptions: EventIdType) -> None:
        for event_id in subscriptions:
            default = EventDelegate("EventStream: {}".format(event_id))
            self.listeners.setdefault(event_id, default).add(action)
