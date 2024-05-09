# pyright: reportPrivateUsage = false

from typing import Optional, Union

from ocsf_diff.compare import _find_ocsf_type
from ocsf_schema import OcsfAttr


def test_find_model():
    assert _find_ocsf_type(OcsfAttr) is OcsfAttr


def test_find_optional():
    assert _find_ocsf_type(Optional[OcsfAttr]) is OcsfAttr


def test_find_dict():
    assert _find_ocsf_type(dict[str, OcsfAttr]) is OcsfAttr


def test_find_optional_dict():
    assert _find_ocsf_type(Optional[dict[str, OcsfAttr]]) is OcsfAttr


def test_find_union():
    assert _find_ocsf_type(Union[OcsfAttr, None]) is OcsfAttr
    assert _find_ocsf_type(Union[None, OcsfAttr]) is OcsfAttr


def test_find_union_dict():
    assert _find_ocsf_type(Union[None, dict[str, OcsfAttr]]) is OcsfAttr
    assert _find_ocsf_type(Union[dict[str, OcsfAttr], None]) is OcsfAttr
