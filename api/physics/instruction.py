from ..scene.system import SceneContent

import abc
from typing import *

_Content = TypeVar("_Content")


# One instance of Instruction is responsible for updating the physics of
# one single instance( target ) of _Content Type
class PhysicsInstruction(Generic[_Content]):
    def __init__(self, target: _Content):
        self.target = target

    @abc.abstractmethod
    def update(self, delta_time: float) -> None:
        pass


_INSTRUCTION_SET: Dict[Type[SceneContent], Type[PhysicsInstruction]] = {}


# Instruction Register
def physics_instruction(content_type: Type[_Content]):
    def decorator(instruction_cls: Type[PhysicsInstruction[_Content]]):
        _INSTRUCTION_SET[content_type] = instruction_cls
        return instruction_cls
    return decorator


def get_instruction(content: _Content) -> Union[None, PhysicsInstruction[_Content]]:
    content_type = type(content)
    if content_type in _INSTRUCTION_SET:
        instruction_type = _INSTRUCTION_SET[content_type]
        instruction: PhysicsInstruction[_Content] = instruction_type(content)
        return instruction
    else:
        return None
