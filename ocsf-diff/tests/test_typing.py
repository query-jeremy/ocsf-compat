
import pytest

from typing import Union, Optional

from ocsf_diff.compare import _resolve_type, _type_info
from ocsf_schema import OcsfModel, OcsfAttr, OcsfEvent

def test_resolve_primitive_type():
    t = int

    origin, args = _type_info(t)
    assert origin == int
    assert len(args) == 0

def test_resolve_ocsf_type():
    t = OcsfAttr

    origin, args = _type_info(t)
    assert origin == OcsfAttr
    assert len(args) == 0

def test_resolve_ocsf_union():
    t = Union[None, OcsfEvent]

    origin, args = _type_info(t)
    assert origin == OcsfEvent
    assert len(args) == 0

def test_resolve_primitive_union():
    t = Union[None, int]

    origin, args = _type_info(t)
    assert origin == int
    assert len(args) == 0

def test_resolve_ocsf_dict():
    t = Optional[OcsfEvent]

    match t:
        case Union[None, model] | Union[mode, None]:
            assert True
        case _:
            assert False

