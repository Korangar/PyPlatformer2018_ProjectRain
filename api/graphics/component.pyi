from ..scene.system import SceneContent
from .camera import Camera

import abc
from typing import *

_Content = TypeVar("_Content")


# One instance of GraphicsInstruction is responsible for drawing one single instance( target ) of _Content Type
class AutoGraphicsComponent(Generic[_Content]):
    sorting: float
    target: _Content

    def __init__(self, target: _Content): ...

    @abc.abstractmethod
    def draw(self, camera: Camera) -> None: ...


_INSTRUCTION_SET: Dict[Type[SceneContent], Type[AutoGraphicsComponent]]


# Instruction Register
def graphics_for(content_type: Type[_Content]) \
        -> Callable[[Type[AutoGraphicsComponent[_Content]]], Type[AutoGraphicsComponent[_Content]]]: ...

def get_component(content: _Content) -> Union[None, AutoGraphicsComponent[_Content]]: ...