from typing import *

_Cls = TypeVar("_Cls")
_Decorator = Callable[[Type[_Cls]], Type[_Cls]]


def assert_on_init(predicate: Callable[[_Cls], bool], msg: str= "") -> _Decorator[_Cls]:
    def decorator(cls: Type[_Cls]) -> Type[_Cls]:
        old_ = getattr(cls, "__new__")

        def new_(self, *args, **kwargs):
            val = old_(self, *args, **kwargs)
            if not predicate(val):
                raise Exception(msg)
            return val
        setattr(cls, "__new__", new_)
        return cls
    return decorator
