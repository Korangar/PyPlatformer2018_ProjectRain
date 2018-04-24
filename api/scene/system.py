from ..events.observer import Observer

from .content import SceneContent, Agent, Player
from .scene_object import SceneObject

from typing import *


on_active_scene_changed: Observer[SceneObject] = Observer("on_active_scene_change")
on_scene_content_added: Observer[Tuple[SceneContent]] = Observer("on_content_create")
on_scene_content_removed: Observer[Tuple[SceneContent]] = Observer("on_content_destroy")

_active_scene: SceneObject = None


def get_active_scene() -> SceneObject:
    return _active_scene


def get_content_by_tag(scene: SceneObject, tag: str) -> Iterable[SceneContent]:
    if tag in scene.tag_dictionary:
        return iter(scene.tag_dictionary[tag])
    else:
        return iter(tuple())


def change_active_scene(scene: SceneObject):
    global _active_scene
    if scene:
        _active_scene = scene
        on_active_scene_changed(_active_scene)


def add_content_to_scene(scene: SceneObject, content: SceneContent) -> None:
    content.scene = scene
    scene.content.add(content)
    if isinstance(content, Player):
        scene.players.add(content)
    if isinstance(content, Agent):
        scene.agents.add(content)
    for tag in content.get_tags():
        scene.tag_dictionary[tag].add(content)
    on_scene_content_added(content)
    content.on_spawn(content)


def remove_content_from_scene(scene: SceneObject, *content: SceneContent):
    # get the prefab that is in the scene
    intersection = scene.content.intersection(content)
    # remove it from the scene
    scene.content.difference_update(intersection)
    for c in intersection:
        c.on_erase(c)
        on_scene_content_removed(c)
        c.scene = None
