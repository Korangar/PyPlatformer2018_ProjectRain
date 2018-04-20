# contextual graphics system
from time import time
from typing import *
from weakref import WeakKeyDictionary

from api.measurement.rate_tracker import RateTracker
from .instruction import PhysicsInstruction, get_instruction
from ..scene import SceneContent, SceneObject, get_active_scene
from ..scene import \
    on_active_scene_changed, \
    on_scene_content_added, \
    on_scene_content_removed

_context_cache: Dict[SceneObject,
                     Dict[SceneContent,
                          PhysicsInstruction]] = WeakKeyDictionary()

_active_context: Dict[SceneContent, PhysicsInstruction] = None

_ups_counter: RateTracker = RateTracker(smoothing_factor=0.1)
_ups_last_measurement: float = time()


# -- public --
#

def get_rate() -> float:
    return _ups_counter.rate


def cache_active_context() -> None:
    # public
    scene = get_active_scene()
    _context_cache[scene] = _active_context


# Update

def update(delta_time: float):
    # public
    global _ups_last_measurement
    now = time()
    _ups_counter.increment()
    if now >= (_ups_last_measurement + 1):
        _ups_counter.measure()
        _ups_last_measurement = now

    # TODO maximize CPU, try multiprocess

    for instruction in _active_context.values():
        instruction.update(delta_time)


# Cleanup

def clear_cache() -> None:
    _context_cache.clear()


def clear_context() -> None:
    _active_context.clear()


# -- private --
#

# EventHandlers

def _handle_scene_change(msg: SceneObject):
    global _active_context
    # get from cache if cached else allocate new context
    if msg in _context_cache:
        # activate context from cache
        _active_context = _context_cache[msg]
    else:
        _active_context = {c: get_instruction(c) for c in msg.content if get_instruction(c)}


def _handle_content_added(msg: SceneContent):
    instruction = get_instruction(msg)
    if instruction:
        # add to active scene or cached context if scene is cached
        if msg.scene == get_active_scene():
            # make instruction for msg and add instruction to context
            _active_context[msg] = instruction
        elif msg.scene in _context_cache:
            # update the cached context with msg
            instructions = _context_cache[msg.scene]
            instructions[msg] = instruction


def _handle_content_removed(msg: SceneContent):
    # remove from active scene or cached context if scene is cached
    if msg.scene == get_active_scene():
        del _active_context[msg]
    elif msg.scene in _context_cache:
        instructions = _context_cache[msg.scene]
        del instructions[msg]


# EventHandler assignment

on_active_scene_changed.observe(_handle_scene_change)
on_scene_content_added.observe(_handle_content_added)
on_scene_content_removed.observe(_handle_content_removed)