from collections import defaultdict
import weakref


class SceneObject:
    def __init__(self, name='', tile_grid=None):
        self.name = name
        self.tile_grid = tile_grid
        self.content = set()
        self.agents = weakref.WeakSet()
        self.players = weakref.WeakSet()
        self.tag_dictionary = defaultdict(weakref.WeakSet)

    def update(self, delta_time: float):
        for p in self.players:
            p.update_will(delta_time)
        for a in self.agents:
            a.update_agency(delta_time)
