
from ocsf_tools.compare import ChangedSchema
from ocsf_tools.validation import Rule, Validator

from .changed_type import NoChangedTypesRule
from .increased_requirement import NoIncreasedRequirementsRule
from .removed_records import NoRemovedRecordsRule

class CompatibilityValidator(Validator[ChangedSchema]):
    def __init__(self, context: ChangedSchema):
        self.context = context

    def rules(self) -> list[Rule[ChangedSchema]]:
        return [
            NoRemovedRecordsRule(),
            NoIncreasedRequirementsRule(),
            NoChangedTypesRule(),
        ]