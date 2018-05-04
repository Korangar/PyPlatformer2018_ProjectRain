from api.sax_engine.core import ContentEntity
from api.sax_engine.vector import Vector2

import abc
from typing import *

_Content = TypeVar("_Content")
_INSTRUCTION_SET: Dict[Type[ContentEntity], Type["AutoPhysicsComponent"]] = {}


# One instance of Instruction is responsible for updating the physics of
# one single instance( target ) of _Content Type
class AutoPhysicsComponent(Generic[_Content]):
    def __init__(self, target: _Content):
        self.target = target
        self.velocity = Vector2(0, 0)

    @abc.abstractmethod
    def update(self) -> None:
        pass


# Instruction Register
def physics_for(content_type: Type[_Content]):
    def decorator(instruction_cls: Type[AutoPhysicsComponent[_Content]]):
        _INSTRUCTION_SET[content_type] = instruction_cls
        return instruction_cls
    return decorator


def get_instruction(content: _Content) -> Union[None, AutoPhysicsComponent[_Content]]:
    content_type = type(content)
    if content_type in _INSTRUCTION_SET:
        instruction_type = _INSTRUCTION_SET[content_type]
        instruction: AutoPhysicsComponent[_Content] = instruction_type(content)
        return instruction
    else:
        return None
