import logging

from dataclasses import dataclass
from enum import StrEnum
from typing import TypeVar, Generic, Optional

LOG = logging.getLogger(__name__)

Context = TypeVar("Context")


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    FATAL = "fatal"


@dataclass(init=False)
class Finding:
    def message(self) -> str:
        raise NotImplementedError()

    def get_severity(self) -> Severity:
        if hasattr(self, "_severity"):
            return self._severity
        else:
            return Severity.ERROR

    def set_severity(self, severity: Severity) -> None:
        self._severity = severity

    def del_severity(self) -> None:
        raise AttributeError("Cannot delete severity")

    severity = property(get_severity, set_severity, del_severity)


@dataclass
class RuleMetadata:
    name: str
    description: str = ""


class Rule(Generic[Context]):
    def __hash__(self):
        return hash(self.__class__)

    def metadata(self) -> RuleMetadata:
        raise NotImplementedError

    def validate(self, context: Context) -> list[Finding]:
        raise NotImplementedError


ValidationFindings = dict[Rule[Context], list[Finding]]


class Validator(Generic[Context]):
    def __init__(self, context: Context, severities: Optional[dict[str, Severity]] = None):
        self.context = context
        self._severities = severities if severities else {}

    def rules(self) -> list[Rule[Context]]:
        raise NotImplementedError()

    def _override_severity(self, finding: Finding) -> None:
        name = finding.__class__.__name__
        if name in self._severities:
            finding.severity = Severity(self._severities[name])

    def validate(self) -> ValidationFindings[Context]:
        findings: ValidationFindings[Context] = {}
        LOG.info("Running validation")

        for rule in self.rules():
            findings[rule] = []
            results = rule.validate(self.context)
            for finding in results:
                self._override_severity(finding)
                findings[rule].append(finding)

            LOG.info(f"Identified {len(results)} findings for rule {rule.metadata().name}")

        return findings


def validate_severities(severities: dict[str, Severity]) -> bool:
    for cls, severity in severities.items():
        if severity not in Severity or cls not in globals():
            raise ValueError(f"Invalid severity value: {cls} = {severity}")

    return True
