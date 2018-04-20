from ..scene.system import SceneContent
from ..utilities.vector import Vector2

from .camera import Camera
from ._pygame_drawing import *

import abc
from typing import *

_Content = TypeVar("_Content")


# One instance of GraphicsInstruction is responsible for drawing one single instance( target ) of _Content Type
class GraphicsInstruction(Generic[_Content]):
    def __init__(self, target: _Content):
        self.sorting = 1
        self.target = target

    @abc.abstractmethod
    def draw(self, camera: Camera) -> None:
        pass


_INSTRUCTION_SET: Dict[Type[SceneContent], Type[GraphicsInstruction]] = {}


# Instruction Register
def graphics_instruction(content_type: Type[_Content]):
    def decorator(instruction_cls: Type[GraphicsInstruction[_Content]]):
        _INSTRUCTION_SET[content_type] = instruction_cls
        return instruction_cls
    return decorator


def get_instruction(content: _Content) -> Union[None, GraphicsInstruction[_Content]]:
    content_type = type(content)
    if content_type in _INSTRUCTION_SET:
        instruction_type = _INSTRUCTION_SET[content_type]
        instruction: GraphicsInstruction[_Content] = instruction_type(content)
        return instruction
    else:
        return None
