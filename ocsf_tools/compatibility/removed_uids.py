"""A validation rule to identify changed class UIDs."""

from dataclasses import dataclass
from ocsf_tools.compare import ChangedSchema, NoChange, ChangedEvent, ChangedAttr, Removal, Addition
from ocsf_tools.validation import Rule, Finding, RuleMetadata

@dataclass
class ChangedClassUidFinding(Finding):
    event: str
    before: str
    after: str

    def message(self) -> str:
        return f"The UID of {self.event} changed from {self.before} to {self.after}"


class NoChangedClassUidsRule(Rule[ChangedSchema]):
    def metadata(self):
        return RuleMetadata("No changed class UIDs")

    def validate(self, context: ChangedSchema) -> list[Finding]:
        findings: list[Finding] = []
        for name, event in context.classes.items():
            if isinstance(event, ChangedEvent):
                if "class_uid" in event.attributes and isinstance(event.attributes["class_uid"], ChangedAttr):
                    uid = event.attributes["class_uid"]
                    if not isinstance(uid.enum, NoChange):
                        before: str | None = None
                        after: str | None = None
                        for k, v in uid.enum.items():
                            if isinstance(v, Removal):
                                before = k
                            elif isinstance(v, Addition):
                                after = k

                        if before is not None and after is not None:
                            findings.append(ChangedClassUidFinding(name, before, after))

        return findings
