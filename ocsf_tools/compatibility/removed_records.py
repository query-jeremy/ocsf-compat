"""A validation rule to identify removed objects, events, attributes, and enums."""

from abc import abstractmethod
from dataclasses import dataclass
from ocsf_tools.schema import OcsfElementType
from ocsf_tools.compare import ChangedSchema, Removal, ChangedEvent, ChangedObject, ChangedAttr
from ocsf_tools.validation import Rule, Finding, RuleMetadata


@dataclass
class RemovedRecordFinding(Finding):
    name: str
    caption: str

    @abstractmethod
    def _kind(self) -> OcsfElementType:
        raise NotImplementedError()

    def message(self) -> str:
        return f"{self._kind()} {self.name} ({self.caption}) was removed"


@dataclass
class RemovedObjectFinding(RemovedRecordFinding):
    def _kind(self):
        return OcsfElementType.OBJECT


@dataclass
class RemovedEventFinding(RemovedRecordFinding):
    def _kind(self):
        return OcsfElementType.EVENT


@dataclass
class RemovedAttrFinding(RemovedRecordFinding):
    parent: tuple[OcsfElementType, str]

    def _kind(self):
        return OcsfElementType.ATTRIBUTE

    def message(self) -> str:
        return f"{self._kind()} {'.'.join(self.parent + (self.name,))} ({self.caption}) was removed"


@dataclass
class RemovedEnumMemberFinding(RemovedRecordFinding):
    parent: tuple[OcsfElementType, str, str]

    def _kind(self):
        return OcsfElementType.ENUM_MEMBER

    def message(self) -> str:
        return f"{self._kind()} {'.'.join(self.parent + (self.name,))} ({self.caption}) was removed"


class NoRemovedRecordsRule(Rule[ChangedSchema]):
    def metadata(self):
        return RuleMetadata("No removed objects or events")

    def validate(self, context: ChangedSchema) -> list[Finding]:
        """Search changed objects and events in the schema to identify any removed elements."""

        findings: list[Finding] = []

        # Look for removed events
        for name, event in context.classes.items():
            if isinstance(event, Removal):
                findings.append(RemovedEventFinding(name, event.before.caption))

            elif isinstance(event, ChangedEvent):
                # While we're here, got any removed attributes?
                for attr_name, attr in event.attributes.items():
                    if isinstance(attr, Removal):
                        findings.append(
                            RemovedAttrFinding(attr_name, attr.before.caption, (OcsfElementType.EVENT, name))
                        )

                    elif isinstance(attr, ChangedAttr):
                        # Or how about removed enum members?
                        if isinstance(attr.enum, dict):
                            for member_key, member in attr.enum.items():
                                if isinstance(member, Removal):
                                    findings.append(
                                        RemovedEnumMemberFinding(
                                            member_key, member.before.caption, (OcsfElementType.EVENT, name, attr_name)
                                        )
                                    )

        # Now do the same as above, but for objects. These two loops could
        # probably be factored together, but this way is more straightforward.
        for name, obj in context.objects.items():
            if isinstance(obj, Removal):
                findings.append(RemovedObjectFinding(name, obj.before.caption))

            elif isinstance(obj, ChangedObject):
                for attr_name, attr in obj.attributes.items():
                    if isinstance(attr, Removal):
                        findings.append(
                            RemovedAttrFinding(attr_name, attr.before.caption, (OcsfElementType.OBJECT, name))
                        )

                    elif isinstance(attr, ChangedAttr):
                        if isinstance(attr.enum, dict):
                            for member_key, member in attr.enum.items():
                                if isinstance(member, Removal):
                                    findings.append(
                                        RemovedEnumMemberFinding(
                                            member_key, member.before.caption, (OcsfElementType.OBJECT, name, attr_name)
                                        )
                                    )

        return findings
