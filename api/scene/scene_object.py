from collections import defaultdict
import weakref


class SceneObject:
    def __init__(self, name='', tile_grid=None):
        self.name = name

        # time
        self.delta_time = 0
        self.current_time = 0

        # environment
        self.tile_grid = tile_grid

        # content
        self.tag_dictionary = defaultdict(weakref.WeakSet)
        self.content = set()
        self.actors = weakref.WeakSet()
