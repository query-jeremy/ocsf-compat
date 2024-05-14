# pyright: reportPrivateUsage = false
from typing import Optional

from ocsf_diff.compare import compare
from ocsf_diff.model import (
    Change,
    NoChange,
    DiffAttr,
    Removal,
    Addition,
)
from ocsf_schema import OcsfAttr, OcsfEnumMember


def test_compare_primitive():
    assert compare(1, 2) == Change(before=1, after=2)
    assert compare(True, False) == Change(before=True, after=False)
    assert compare(True, True) == NoChange[bool]()
    assert compare([1, 2, 3], [1, 2]) == Change(before=[1, 2, 3], after=[1, 2])

    x1: Optional[bool] = True
    x2: Optional[bool] = None
    assert compare(x1, x2) == Change(True, None)


def test_compare_scalar():
    old_attr = OcsfAttr(caption="test1", description="", requirement="required", type="int_t")
    new_attr = OcsfAttr(caption="test2", description="", requirement="required", type="int_t")
    diff = compare(old_attr, new_attr)

    assert isinstance(diff, DiffAttr)
    assert diff.caption == Change(before="test1", after="test2")
    assert diff.description == NoChange()
    assert diff.requirement == NoChange()
    assert diff.enum == {} #NoChange()


def test_compare_optional_change():
    old_attr = OcsfAttr(caption="test1", group=None, description="", requirement="required", type="int_t")
    new_attr = OcsfAttr(caption="test2", group="test", description="", requirement="required", type="int_t")
    diff = compare(old_attr, new_attr)

    assert isinstance(diff, DiffAttr)
    assert diff.group== Change(before=None, after="test")


def test_optional_dict():
    old_attr = OcsfAttr(
        caption="test",
        description="",
        requirement="required",
        type="int_t",
        enum={
            "1": OcsfEnumMember(caption="Other"),
            "-1": OcsfEnumMember(caption="Unknown"),
        },
    )
    new_attr = OcsfAttr(
        caption="test",
        description="",
        requirement="required",
        type="int_t",
        enum={
            "1": OcsfEnumMember(caption="Other"),
            "99": OcsfEnumMember(caption="Unknown"),
        },
    )

    diff = compare(old_attr, new_attr)
    assert isinstance(diff, DiffAttr)
    assert diff.caption == NoChange()

    assert isinstance(diff.enum, dict)
    assert "1" in diff.enum
    assert "-1" in diff.enum
    assert "99" in diff.enum
    assert diff.enum["-1"] == Removal(before=OcsfEnumMember(caption="Unknown"))
    assert diff.enum["1"] == NoChange()
    assert diff.enum["99"] == Addition(after=OcsfEnumMember(caption="Unknown"))


def test_empty_dict():
    """
    old_dict = OcsfDictionaryTypes(caption="old", description="Old", attributes={})
    new_dict = OcsfDictionaryTypes(caption="new", description="New", attributes={})
    diff = compare(old_dict, new_dict)
    assert diff.caption == Change[str](before="old", after="new")
    assert diff.attributes == {}
    """

def test_dict():
    """
    old_dict = OcsfDictionaryTypes(
        caption="types",
        description="Types",
        attributes={
            "src_endpoint": OcsfAttr(caption="Source Endpoint"),
            "dst_endpoint": OcsfAttr(caption="Dst Endpoint"),
            "relevance": OcsfAttr(type="int_t"),
        },
    )
    new_dict = OcsfDictionaryTypes(
        caption="types",
        description="New Types",
        attributes={
            "src_endpoint": OcsfAttr(caption="Source Endpoint"),
            "dst_endpoint": OcsfAttr(caption="Destination Endpoint"),
            "signature": OcsfAttr(caption="signature"),
        },
    )

    diff = compare(old_dict, new_dict)
    assert isinstance(diff, DiffDictionaryTypes)
    assert diff.caption == NoChange[str]()
    assert diff.description == Change[str](before="Types", after="New Types")

    assert isinstance(diff.attributes, dict)
    for attr in ("src_endpoint", "relevance", "signature", "dst_endpoint"):
        assert attr in diff.attributes

    assert diff.attributes["src_endpoint"] == NoChange[OcsfAttr]()
    assert diff.attributes["signature"] == Addition[OcsfAttr](after=OcsfAttr(caption="signature"))
    assert diff.attributes["relevance"] == Removal[OcsfAttr](before=OcsfAttr(type="int_t"))
    assert diff.attributes["dst_endpoint"] == DiffAttr(
        caption=Change[Optional[str]](before="Dst Endpoint", after="Destination Endpoint")
    )
    """
