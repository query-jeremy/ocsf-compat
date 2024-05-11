from typing import overload, TypeVar

from ocsf_schema.model import (
    OcsfSchema,
    OcsfCategory,
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
    OcsfModel,
)
from ocsf_diff.model import (
    DiffSchema,
    DiffEvent,
    DiffCategory,
    DiffObject,
    DiffAttr,
    DiffDeprecationInfo,
    ChangedModel,
    DiffDictionary,
    DiffDictionaryTypes,
    DiffCategories,
    DiffInclude,
    DiffProfile,
    DiffExtension,
    DiffVersion,
    DiffEnumMember,
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
def create_diff(model: OcsfCategory) -> DiffCategory: ...


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

T = TypeVar("T", bound=OcsfModel)

def create_diff(model: T) -> ChangedModel[T]:
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
        case OcsfCategory():
            return DiffCategory()
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
        case _:
            raise ValueError("What model be this?")
