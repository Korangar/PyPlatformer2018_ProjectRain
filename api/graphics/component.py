

# One instance of GraphicsInstruction is responsible for drawing one single instance( target ) of _Content Type
class AutoGraphicsComponent:
    def __init__(self, target):
        self.sorting = 1
        self.target = target

    def draw(self, camera) -> None:
        pass


_INSTRUCTION_SET = {}


# Instruction Register
def graphics_for(content_type):
    def decorator(instruction_cls):
        _INSTRUCTION_SET[content_type] = instruction_cls
        return instruction_cls
    return decorator


def get_component(content):
    content_type = type(content)
    if content_type in _INSTRUCTION_SET:
        instruction_type = _INSTRUCTION_SET[content_type]
        instruction = instruction_type(content)
        return instruction
    else:
        return None
