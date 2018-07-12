from api.sax_engine.core.entities import ActorEntity
from api.sax_engine.geometry import Point

from api.sax_engine.events.event import Event
from api.sax_engine.events.event_stream import EventStream
from api.sax_engine.core.systems.state.machine import StateMachine
from api.sax_engine.vector import *

from .event_id import EventId
from .data import *


__all__ = ["PreAlphaTier"]


class PreAlphaTier(ActorEntity):
    def __init__(self, n=0, position=Point(0, 0)):
        super().__init__(position)
        self.number = n
        # data
        self.physics_data: PhysicsData = PhysicsData()
        self.shared_data: SharedData = SharedData()
        self.graphics_data: GraphicsData = GraphicsData()
        # events
        self.event_stream = EventStream(verbose=False)
        # state
        from .components.state.states import create_states
        self.state_machine = StateMachine(*create_states(self))

    def push_event(self, event, **kwargs):
        self.event_stream.push(Event(event, self.scene.current_time, kwargs))

    def spawn(self):
        self.push_event(EventId.actor_spawn)

        self.state_machine.set_state(self.shared_data.DEFAULT_STATE)
        self.physics_data.size = Vector2(1.2, 0.6)

    def update(self):
        self.state_machine.update()
        pass
