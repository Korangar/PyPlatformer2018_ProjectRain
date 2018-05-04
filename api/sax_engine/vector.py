import math
from typing import *

Vector = Union[Tuple[float, ...], Tuple[int, ...]]


class Vector2(NamedTuple):
    x: float
    y: float

    def to_int(self) -> Tuple[int, int]:
        return int(self.x), int(self.y)


VectorType = Union[Vector2, Vector]
ScalarOrVector = Union[int, float, VectorType]


# noinspection SpellCheckingInspection
def v_lenq(v: VectorType) -> float:
    return sum(vi * vi for vi in v)


def v_len(v: VectorType) -> float:
    return math.sqrt(v_lenq(v))


def v_dot(v1: VectorType, v2: VectorType) -> float:
    return sum((vi[0] * vi[1]) for vi in zip(v1, v2))


def v_add(*v: VectorType) -> VectorType:
    return tuple(sum(vi) for vi in zip(*v))


def v_sub(*v: VectorType) -> VectorType:
    return tuple(vi[0] - sum(vi[1:]) for vi in zip(*v))


def v_mul(v: VectorType, m: ScalarOrVector) -> VectorType:
    if isinstance(m, (int, float)):
        r = (i * m for i in v)
    else:
        r = (i * j for i, j in zip(v, m))
    return tuple(r)


def v_div(v: VectorType, d: ScalarOrVector) -> VectorType:
    if isinstance(d, (int, float)):
        r = (i / d for i in v)
    else:
        r = (i / j for i, j in zip(v, d))
    return tuple(r)


def v_min(*v: VectorType) -> VectorType:
    return tuple(min(vi) for vi in zip(*v))


def v_max(*v: VectorType) -> VectorType:
    return tuple(max(vi) for vi in zip(*v))


def v_norm(v: VectorType) -> VectorType:
    return v_mul(v, 1 / v_len(v))


def v_ceil(v: VectorType) -> VectorType:
    return tuple(math.ceil(i) for i in v)


def v_floor(v: VectorType) -> VectorType:
    return tuple(math.floor(i) for i in v)
