from typing import cast

from ocsf_schema.model import (
    OcsfSchema,
    OcsfEvent,
    OcsfObject,
    OcsfAttr,
    OcsfDeprecationInfo,
    OcsfType,
    OcsfVersion,
    OcsfEnumMember,
    OcsfT,
)
from ocsf_diff.model import (
    DiffSchema,
    DiffEvent,
    DiffObject,
    DiffAttr,
    DiffDeprecationInfo,
    ChangedModel,
    DiffType,
    DiffVersion,
    DiffEnumMember,
)


def create_diff(model: OcsfT) -> ChangedModel[OcsfT]:
    match model:
        case OcsfSchema():
            ret = DiffSchema()
        case OcsfEvent():
            ret = DiffEvent()
        case OcsfObject():
            ret = DiffObject()
        case OcsfAttr():
            ret = DiffAttr()
        case OcsfDeprecationInfo():
            ret = DiffDeprecationInfo()
        case OcsfVersion():
            ret = DiffVersion()
        case OcsfEnumMember():
            ret = DiffEnumMember()
        case OcsfType():
            ret = DiffType()
        case _:
            raise ValueError("Unrecognized OCSF model type")

    return cast(ChangedModel[OcsfT], ret)
