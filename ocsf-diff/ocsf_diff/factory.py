from typing import overload

from ocsf_schema.model import (
    OcsfSchema,
    OcsfEvent,
    OcsfObject,
    OcsfAttr,
    OcsfDeprecationInfo,
    OcsfDictionary,
    OcsfDictionaryTypes,
    OcsfCategories,
    OcsfInclude,
    OcsfProfile,
    OcsfExtension,
    OcsfVersion,
    OcsfEnumMember,
)
from ocsf_diff.model import (
    DiffSchema,
    DiffEvent,
    DiffObject,
    DiffAttr,
    DiffDeprecationInfo,
    DiffModel,
    DiffDictionary,
    DiffDictionaryTypes,
    DiffCategories,
    DiffInclude,
    DiffProfile,
    DiffExtension,
    DiffVersion,
    DiffEnumMember,
    OcsfComparable,
)


@overload
def create_diff(model: OcsfSchema) -> DiffSchema: ...


@overload
def create_diff(model: OcsfEvent) -> DiffEvent: ...


@overload
def create_diff(model: OcsfObject) -> DiffObject: ...


@overload
def create_diff(model: OcsfAttr) -> DiffAttr: ...


@overload
def create_diff(model: OcsfDeprecationInfo) -> DiffDeprecationInfo: ...


@overload
def create_diff(model: OcsfDictionary) -> DiffDictionary: ...


@overload
def create_diff(model: OcsfCategories) -> DiffCategories: ...


@overload
def create_diff(model: OcsfInclude) -> DiffInclude: ...


@overload
def create_diff(model: OcsfProfile) -> DiffProfile: ...


@overload
def create_diff(model: OcsfExtension) -> DiffExtension: ...


@overload
def create_diff(model: OcsfVersion) -> DiffVersion: ...


@overload
def create_diff(model: OcsfEnumMember) -> DiffEnumMember: ...


@overload
def create_diff(model: OcsfDictionaryTypes) -> DiffDictionaryTypes: ...


def create_diff(model: OcsfComparable) -> DiffModel:
    match model:
        case OcsfSchema():
            return DiffSchema()
        case OcsfEvent():
            return DiffEvent()
        case OcsfObject():
            return DiffObject()
        case OcsfAttr():
            return DiffAttr()
        case OcsfDeprecationInfo():
            return DiffDeprecationInfo()
        case OcsfDictionary():
            return DiffDictionary()
        case OcsfCategories():
            return DiffCategories()
        case OcsfInclude():
            return DiffInclude()
        case OcsfProfile():
            return DiffProfile()
        case OcsfExtension():
            return DiffExtension()
        case OcsfVersion():
            return DiffVersion()
        case OcsfEnumMember():
            return DiffEnumMember()
        case OcsfDictionaryTypes():
            return DiffDictionaryTypes()
