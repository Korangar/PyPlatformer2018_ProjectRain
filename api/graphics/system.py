# contextual graphics system
from time import time
from typing import *
from weakref import WeakKeyDictionary

from api.measurement.rate_tracker import RateTracker
from ._pygame_display import PyGameDisplay
from ._pygame_drawing import gfxdraw, C_RED, C_BLUE, C_GREEN, C_YELLOW
from .camera import Camera
from .instruction import GraphicsInstruction, get_instruction
from ..scene import SceneContent, SceneObject, get_active_scene
from ..scene import \
    on_active_scene_changed, \
    on_scene_content_added, \
    on_scene_content_removed
from ..utilities.projection import Projection
from ..utilities.vector import *

_display: PyGameDisplay = None

_context_cache: Dict[SceneObject,
                     Tuple[List[Camera],
                           Dict[SceneContent,
                                GraphicsInstruction]]] = WeakKeyDictionary()

_active_cameras: List[Camera] = None
_active_sorting: List[GraphicsInstruction] = None
_active_context: Dict[SceneContent, GraphicsInstruction] = None

_fps_counter: RateTracker = RateTracker()
_fps_last_measurement: float = time()


# -- public --
#

# Getters
def get_display() -> PyGameDisplay:
    # public
    return _display


def get_cameras() -> List[Camera]:
    # public
    return _active_cameras


def get_rate() -> float:
    return _fps_counter.rate


def init_display(resolution: Tuple[int, int]=(0, 0), depth: int = 0, full_screen: bool = True):
    # public
    global _display
    _display = PyGameDisplay(resolution, depth, full_screen)


def cache_active_context() -> None:
    # public
    scene = get_active_scene()
    _context_cache[scene] = [_active_cameras, _active_context]


def add_camera(anchor: SceneContent,
               target_dim: Vector2,
               pixels_per_tile: int= 32,
               source_rel_off: Vector2= Vector2(0, 0),
               target_rel_off: Vector2= Vector2(0, 0),
               cam_id: str=""):
    # public
    source_dim = Vector2(*v_div(target_dim, pixels_per_tile))
    source_off = Vector2(*v_mul(source_dim, source_rel_off))
    target_off = Vector2(*v_mul(target_dim, target_rel_off))
    # target offset not required in projection, because of the subsurface
    projection = Projection(source_dim=source_dim,
                            source_off=source_off,
                            target_dim=target_dim,
                            target_off=Vector2(0, 0),
                            inverse_h=False,
                            inverse_v=True)
    render_target = _display.canvas.subsurface((target_off, target_dim))
    _active_cameras.append(Camera(cam_id, projection, anchor, render_target, pixels_per_tile))


# Update

def update():
    # public
    global _fps_last_measurement
    now = time()
    _fps_counter.increment()
    if now >= (_fps_last_measurement + 1):
        _fps_counter.measure()
        _fps_last_measurement = now

    # TODO maximize CPU, make rendering multiprocess
    # TODO need proper layered rendering

    for camera in _active_cameras:
        for instruction in _active_sorting:
            instruction.draw(camera)

    _display.flip()


# Cleanup

def clear_cache() -> None:
    _context_cache.clear()


def clear_cameras() -> None:
    _active_cameras.clear()


def clear_context() -> None:
    _active_context.clear()


# -- private --
#

# EventHandlers

def _handle_scene_change(msg: SceneObject):
    global _active_context, _active_cameras, _active_sorting
    if msg in _context_cache:
        # activate context from cache
        _active_cameras, _active_context = _context_cache[msg]
    else:
        _active_cameras = list()
        _active_context = {c: get_instruction(c) for c in msg.content if get_instruction(c)}
    # assemble an initial sorting
    _active_sorting = list(_active_context.values())
    _active_sorting.sort(key=lambda s: s.sorting)


def _handle_content_added(msg: SceneContent):
    if msg.scene == get_active_scene():
        # make instruction for msg and add instruction to context
        instruction = get_instruction(msg)
        if instruction:
            _active_context[msg] = instruction
            # update active sorting
            _active_sorting.append(instruction)
            _active_sorting.sort(key=lambda s: s.sorting)
    elif msg.scene in _context_cache:
        # update the cached context with msg
        cameras, instructions = _context_cache[msg.scene]
        instructions[msg] = get_instruction(msg)


def _handle_content_removed(msg: SceneContent):
    if msg.scene == get_active_scene():
        _active_sorting.remove(_active_context[msg])
        del _active_context[msg]
    elif msg.scene in _context_cache:
        cameras, instructions = _context_cache[msg.scene]
        del instructions[msg]


# EventHandler assignment

on_active_scene_changed.observe(_handle_scene_change)
on_scene_content_added.observe(_handle_content_added)
on_scene_content_removed.observe(_handle_content_removed)
