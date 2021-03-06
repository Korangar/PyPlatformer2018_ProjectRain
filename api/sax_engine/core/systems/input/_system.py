from typing import *
from weakref import WeakKeyDictionary

from .component import AutoInputComponent, get_instruction
from api.sax_engine.core import ContentEntity, SceneObject, get_active_scene
from api.sax_engine.core import \
    on_active_scene_changed, \
    on_scene_content_added, \
    on_scene_content_removed


_context_cache: Dict[SceneObject,
                     Dict[ContentEntity,
                          AutoInputComponent]] = WeakKeyDictionary()

_active_context: Dict[ContentEntity, AutoInputComponent] = None


# -- public --
#
def cache_active_context() -> None:
    # public
    scene = get_active_scene()
    _context_cache[scene] = _active_context


# Update
def update():
    # public
    for instruction in _active_context.values():
        instruction.update()


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


def _handle_content_added(msg: ContentEntity):
    instruction = get_instruction(msg)
    if instruction:
        # add to active core or cached context if core is cached
        if msg.scene == get_active_scene():
            # make instruction for msg and add instruction to context
            _active_context[msg] = instruction
        elif msg.scene in _context_cache:
            # update the cached context with msg
            instructions = _context_cache[msg.scene]
            instructions[msg] = instruction


def _handle_content_removed(msg: ContentEntity):
    # remove from active core or cached context if core is cached
    if msg.scene == get_active_scene():
        context = _active_context
    elif msg.scene in _context_cache:
        context = _context_cache[msg.scene]
    else:
        return None

    if msg in context:
        del context[msg]


# EventHandler assignment

on_active_scene_changed.add(_handle_scene_change)
on_scene_content_added.add(_handle_content_added)
on_scene_content_removed.add(_handle_content_removed)
