
from dataclasses import dataclass
from ocsf_tools.compare import ChangedSchema, Removal
from ocsf_tools.validation import Rule, Finding, RuleMetadata

@dataclass
class RemovedRecordFinding(Finding):
    name: str
    caption: str

    def _kind(self) -> str:
        raise NotImplementedError()
    
    def message(self) -> str:
        return f"{self._kind()} {self.name} ({self.caption}) was removed"

class RemovedObjectFinding(RemovedRecordFinding):
    def _kind(self) -> str:
        return "Object"

class RemovedEventFinding(RemovedRecordFinding):
    def _kind(self) -> str:
        return "Event"


class NoRemovedRecordsRule(Rule[ChangedSchema]):
    def metadata(self):
        return RuleMetadata("No removed objects or events")

    def validate(self, context: ChangedSchema) -> list[Finding]:
        findings: list[Finding] = []
        for name, event in context.classes.items():
            if isinstance(event, Removal):
                findings.append(RemovedEventFinding(name, event.before.caption))

        for name, obj in context.objects.items():
            if isinstance(obj, Removal):
                findings.append(RemovedObjectFinding(name, obj.before.caption))

        return findings