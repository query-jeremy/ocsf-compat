
from typing import Optional
from .validator import Finding, Severity, ValidationFindings, Context

class FindingFormatter:
    def __init__(self, severities: Optional[dict[Severity, str]] = None):
        self._severities = severities if severities else {}

    def severity(self, finding: Finding) -> Severity:
        name = finding.__class__.__name__
        if name in self._severities:
            return Severity(self._severities[name])

        raise ValueError(f"No severity found for {name}")

    def format(self, finding: Finding) -> str:
        return f"  [{self.severity(finding)}] {finding.message()}"


class ValidationFormatter:
    def __init__(self, finding_formatter: FindingFormatter):
        self._finding_formatter = finding_formatter

    def format(self, findings: ValidationFindings[Context]) -> str:
        output = ""
        for rule, rule_findings in findings.items():
            name = rule.metadata().name
            output += f"{name}\n"
            output += "=" * len(name) + "\n"

            for finding in rule_findings:
                output += self._finding_formatter.format(finding) + "\n"

        return output