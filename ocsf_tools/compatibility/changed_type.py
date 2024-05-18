"""A validation rule to identify changed attribute types."""
from dataclasses import dataclass
from ocsf_tools.compare import ChangedSchema, Change, ChangedEvent, ChangedObject, ChangedAttr
from ocsf_tools.schema import OcsfElementType
from ocsf_tools.validation import Rule, Finding, RuleMetadata


@dataclass
class ChangedTypeFinding(Finding):
    element_type: OcsfElementType
    record: str
    attr: str
    before: str | None
    after: str | None

    def message(self) -> str:
        return f"Type of {self.element_type} {self.record}.{self.attr} changed from {self.before} to {self.after}"


class NoChangedTypesRule(Rule[ChangedSchema]):
    def metadata(self):
        return RuleMetadata("No changed attribute types")

    def validate(self, context: ChangedSchema) -> list[Finding]:
        findings: list[Finding] = []
        for name, event in context.classes.items():
            if isinstance(event, ChangedEvent):
                for attr_name, attr in event.attributes.items():
                    if isinstance(attr, ChangedAttr):
                        if isinstance(attr.type, Change):
                            findings.append(
                                ChangedTypeFinding(
                                    OcsfElementType.EVENT, name, attr_name, attr.type.before, attr.type.after
                                )
                            )

        for name, obj in context.objects.items():
            if isinstance(obj, ChangedObject):
                for attr_name, attr in obj.attributes.items():
                    if isinstance(attr, ChangedAttr):
                        if isinstance(attr.type, Change):
                            findings.append(
                                ChangedTypeFinding(
                                    OcsfElementType.OBJECT, name, attr_name, attr.type.before, attr.type.after
                                )
                            )

        return findings
