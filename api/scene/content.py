from ..utilities.geometry import *
from ..events.observer import Observer


class SceneContent:
    def __init__(self, position=Point(0, 0)):
        self._tags = list()
        self.scene = None
        self.children = []
        self.position = position
        name = type(self).__name__
        self.on_spawn = Observer("{} spawned!".format(name))
        self.on_erase = Observer("{} erased!".format(name))

    def __repr__(self):
        return "<{}@{}>".format(super().__repr__(), self.scene)

    def get_tags(self):
        return self._tags


class Agent(SceneContent):
    def __init__(self, position):
        super(SceneContent).__init__(position)

    def update_agency(self, delta_time):
        pass


class Player(Agent):
    def __init__(self, position):
        super(Agent).__init__(position)

    def update_will(self, delta_time):
        pass
