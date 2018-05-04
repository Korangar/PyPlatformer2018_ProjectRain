from api.sax_engine.events.event_delegate import EventDelegate

from .entities import ContentEntity, ActorEntity
from .scene_object import SceneObject

from typing import *


on_active_scene_changed: EventDelegate[SceneObject] = EventDelegate("on_active_scene_change")
on_scene_content_added: EventDelegate[Tuple[ContentEntity]] = EventDelegate("on_content_create")
on_scene_content_removed: EventDelegate[Tuple[ContentEntity]] = EventDelegate("on_content_destroy")

_active_scene: SceneObject = None


def get_active_scene() -> SceneObject:
    return _active_scene


def get_content_by_tag(scene: SceneObject, tag: str) -> Iterable[ContentEntity]:
    if tag in scene.tag_dictionary:
        return iter(scene.tag_dictionary[tag])
    else:
        return iter(tuple())


def set_delta_time(delta_time: float):
    _active_scene.delta_time = delta_time
    _active_scene.current_time += delta_time


def update():
    for a in _active_scene.actors:
        a.update()


def change_active_scene(scene: SceneObject):
    global _active_scene
    if scene:
        _active_scene = scene
        on_active_scene_changed(_active_scene)


def add_content_to_scene(scene: SceneObject, content: ContentEntity) -> None:
    content.scene = scene
    scene.content.add(content)
    if isinstance(content, ActorEntity):
        scene.actors.add(content)
    for tag in content.get_tags():
        scene.tag_dictionary[tag].add(content)
    on_scene_content_added(content)
    content.spawn()


def remove_content_from_scene(scene: SceneObject, *content: ContentEntity):
    # get the prefabs that is in the core
    intersection = scene.content.intersection(content)
    # remove it from the core
    scene.content.difference_update(intersection)
    for c in intersection:
        c.destroy()
        on_scene_content_removed(c)
        c.scene = None
