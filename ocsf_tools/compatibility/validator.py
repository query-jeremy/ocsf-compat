"""A backwards compatibility validator."""

from ocsf_tools.compare import ChangedSchema
from ocsf_tools.validation import Rule, Validator

from .changed_type import NoChangedTypesRule
from .increased_requirement import NoIncreasedRequirementsRule
from .removed_records import NoRemovedRecordsRule
from .removed_uids import NoChangedClassUidsRule


class CompatibilityValidator(Validator[ChangedSchema]):
    def rules(self) -> list[Rule[ChangedSchema]]:
        return [
            NoRemovedRecordsRule(),
            NoChangedClassUidsRule(),
            NoIncreasedRequirementsRule(),
            NoChangedTypesRule(),
        ]
