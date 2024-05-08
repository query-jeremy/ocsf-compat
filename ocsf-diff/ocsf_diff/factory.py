from typing import overload

from ocsf_schema.model import (
    OcsfSchema,
    OcsfEvent,
    OcsfObject,
    OcsfAttr,
    OcsfDeprecationInfo,
    OcsfModel,
    OcsfDictionary,
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
def create_diff(model: OcsfModel) -> DiffModel: ...


def create_diff(model: OcsfModel) -> DiffModel:
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
        case _:
            t = type(model)
            raise ValueError(f"Unrecognized model type: {t}")
