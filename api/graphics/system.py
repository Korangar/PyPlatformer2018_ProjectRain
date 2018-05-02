# contextual graphics system
from ..utilities.vector import *
from ..measurement.rate_tracker import RateTracker
from ..scene import SceneContent, SceneObject, get_active_scene
from ..scene import \
    on_active_scene_changed, \
    on_scene_content_added, \
    on_scene_content_removed

from .display import PyGameDisplay
from .camera import Camera, RenderTarget
from .component import AutoGraphicsComponent, get_component

from time import time
from weakref import WeakKeyDictionary

_display: PyGameDisplay = None

_context_cache: Dict[SceneObject,
                     Tuple[List[Camera],
                           Dict[SceneContent,
                                AutoGraphicsComponent]]] = WeakKeyDictionary()

_active_cameras: List[Camera] = None
_active_sorting: List[AutoGraphicsComponent] = None
_active_context: Dict[SceneContent, AutoGraphicsComponent] = None

_fps_counter: RateTracker = RateTracker()
_fps_last_measurement: float = time()


# --- public ---

# - Getter
def get_display() -> PyGameDisplay:
    return _display


def get_cameras() -> Sequence[Camera]:
    return _active_cameras


def get_rate() -> float:
    return _fps_counter.rate


# - Initializer
def init_display(resolution: Tuple[int, int]=(0, 0), depth: int = 0, full_screen: bool = True):
    global _display
    _display = PyGameDisplay(resolution, depth, full_screen)


def cache_active_context() -> None:
    scene = get_active_scene()
    _context_cache[scene] = [_active_cameras, _active_context]


def get_camera_setup(n_split: int=0) -> Iterator[RenderTarget]:
    # creates initializers for any usual screen setup
    assert 0 <= n_split <= 2
    # determine screen and view size depending on the number of splits
    if n_split == 2:
        split = 0.5, 0.5
    elif n_split == 1:
        split = 0.5, 1.0
    else:
        split = 1.0, 1.0
    s_size = Vector2(*v_mul(_display.resolution, split))
    # create render targets
    relative_screen_positions = [(0, 0)]
    if n_split >= 1:
        relative_screen_positions.append((1, 0))
    if n_split >= 2:
        relative_screen_positions.append((0, 1))
        relative_screen_positions.append((1, 1))

    temp = (_create_subsurface((Vector2(*v_mul(s_size, r)).to_int(), s_size.to_int()))
            for r in relative_screen_positions)
    return temp


# - Reset
def clear_cache() -> None:
    _context_cache.clear()


def clear_cameras() -> None:
    _active_cameras.clear()


def clear_context() -> None:
    _active_context.clear()


# - Update
def update():
    global _fps_last_measurement
    now = time()
    _fps_counter.increment()
    if now >= (_fps_last_measurement + 1):
        _fps_counter.measure()
        _fps_last_measurement = now
        print("fps: {:2f}".format(_fps_counter.rate))

    # TODO maximize CPU, make rendering multiprocess
    for c in _active_cameras:
        c.render(_active_sorting)

    _display.flip()


# --- private ---

def _create_subsurface(rect):
    return _display.canvas.subsurface(rect)


# - EventHandlers
def _handle_scene_change(msg: SceneObject):
    global _active_context, _active_cameras, _active_sorting
    if msg in _context_cache:
        # activate context from cache
        _active_cameras, _active_context = _context_cache[msg]
    else:
        _active_cameras = [c for c in msg.content if isinstance(c, Camera)]
        _active_context = {c: get_component(c) for c in msg.content if get_component(c)}
    # assemble an initial sorting
    _active_sorting = list(_active_context.values())
    _active_sorting.sort(key=lambda s: s.sorting)


def _handle_content_added(msg: SceneContent):
    in_active_scene = msg.scene == get_active_scene()

    # select target context
    if in_active_scene:
        # active context
        cameras, context = _active_cameras, _active_context
    elif msg.scene in _context_cache:
        # not active but cached context
        cameras, context = _context_cache[msg.scene]
    else:
        # not in any relevant context
        return None

    # check if it is a camera
    if isinstance(msg, Camera):
        # todo hand over some rendering target
        _active_cameras.append(msg)

    # look for a component for content
    component = get_component(msg)
    if component:
        # add component to context
        context[msg] = component
        # update sorting if necessary
        if in_active_scene:
            _active_sorting.append(component)
            _active_sorting.sort(key=lambda s: s.sorting)


def _handle_content_removed(msg: SceneContent):
    in_active_scene = msg.scene == get_active_scene()

    # select target context
    if in_active_scene:
        # active context
        cameras, context = _active_cameras, _active_context
    elif msg.scene in _context_cache:
        # not active but cached context
        cameras, context = _context_cache[msg.scene]
    else:
        # not in any relevant context
        return None

    # check if it is a camera
    if isinstance(msg, Camera):
        cameras.remove(msg)
        # todo other camera stuff

    # look for a component
    if msg in context:
        # update sorting if necessary
        if in_active_scene:
            _active_sorting.remove(context[msg])
        # remove component from context
        del context[msg]


# EventHandler assignment
on_active_scene_changed.add(_handle_scene_change)
on_scene_content_added.add(_handle_content_added)
on_scene_content_removed.add(_handle_content_removed)
