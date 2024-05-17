from dataclasses import dataclass

from ocsf_tools.compare import ChangedSchema, Removal, Change, ChangedEvent, ChangedObject, ChangedAttr
from ocsf_tools.schema import OcsfElementType

from .validator import Rule, Validator, Finding, RuleMetadata


@dataclass
class CompatibilityContext:
    difference: ChangedSchema


@dataclass
class RemovedRecordFinding(Finding):
    element_type: OcsfElementType
    name: str
    caption: str

    def message(self) -> str:
        return f"{self.element_type} {self.name} ({self.caption}) was removed"


class NoRemovedRecordsRule(Rule[CompatibilityContext]):
    def metadata(self):
        return RuleMetadata("No removed objects or events")

    def validate(self, context: CompatibilityContext) -> list[Finding]:
        findings: list[Finding] = []
        for name, event in context.difference.classes.items():
            if isinstance(event, Removal):
                findings.append(RemovedRecordFinding(OcsfElementType.EVENT, name, event.before.caption))

        for name, obj in context.difference.objects.items():
            if isinstance(obj, Removal):
                findings.append(RemovedRecordFinding(OcsfElementType.OBJECT, name, obj.before.caption))

        return findings


@dataclass
class ChangedRequirementFinding(Finding):
    element_type: OcsfElementType
    path: tuple[str, str]
    before: str | None
    after: str

    def message(self) -> str:
        return f"Requirement of {self.element_type} {'.'.join(self.path)} changed from {self.before} to {self.after}"


class NoIncreasedRequirementsRule(Rule[CompatibilityContext]):
    def metadata(self):
        return RuleMetadata("No increased requirements")

    def validate(self, context: CompatibilityContext) -> list[Finding]:
        findings: list[Finding] = []
        for name, event in context.difference.classes.items():
            if isinstance(event, ChangedEvent):
                for attr_name, attr in event.attributes.items():
                    if isinstance(attr, ChangedAttr):
                        if isinstance(attr.requirement, Change) and attr.requirement.after == "required":
                            findings.append(
                                ChangedRequirementFinding(
                                    OcsfElementType.EVENT,
                                    (name, attr_name),
                                    attr.requirement.before,
                                    attr.requirement.after,
                                )
                            )

        for name, obj in context.difference.objects.items():
            if isinstance(obj, ChangedObject):
                for attr_name, attr in obj.attributes.items():
                    if isinstance(attr, ChangedAttr):
                        if isinstance(attr.requirement, Change) and attr.requirement.after == "required":
                            findings.append(
                                ChangedRequirementFinding(
                                    OcsfElementType.OBJECT,
                                    (name, attr_name),
                                    attr.requirement.before,
                                    attr.requirement.after,
                                )
                            )

        return findings


@dataclass
class ChangedTypeFinding(Finding):
    element_type: OcsfElementType
    record: str
    attr: str
    before: str | None
    after: str | None

    def message(self) -> str:
        return f"Type of {self.element_type} {self.record}.{self.attr} changed from {self.before} to {self.after}"


class NoChangedTypesRule(Rule[CompatibilityContext]):
    def metadata(self):
        return RuleMetadata("No changed attribute types")

    def validate(self, context: CompatibilityContext) -> list[Finding]:
        findings: list[Finding] = []
        for name, event in context.difference.classes.items():
            if isinstance(event, ChangedEvent):
                for attr_name, attr in event.attributes.items():
                    if isinstance(attr, ChangedAttr):
                        if isinstance(attr.type, Change):
                            findings.append(
                                ChangedTypeFinding(
                                    OcsfElementType.EVENT, name, attr_name, attr.type.before, attr.type.after
                                )
                            )

        for name, obj in context.difference.objects.items():
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


class CompatibilityValidator(Validator[CompatibilityContext]):
    def __init__(self, context: CompatibilityContext):
        self.context = context

    def rules(self) -> list[Rule[CompatibilityContext]]:
        return [
            NoRemovedRecordsRule(),
            NoIncreasedRequirementsRule(),
            NoChangedTypesRule(),
        ]
