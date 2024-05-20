from textwrap import wrap
from typing import Literal
from termcolor import colored
from .validator import Finding, ValidationFindings, Context, Severity


class ValidationFormatter:
    def format_finding(self, finding: Finding) -> str:
        return f"  [{finding.severity.upper()}] {finding.message()}"

    def format(self, findings: ValidationFindings[Context]) -> str:
        output = ""
        for rule, rule_findings in findings.items():
            name = rule.metadata().name
            output += "=" * len(name) + "\n"
            output += f"{name}\n"
            output += "=" * len(name) + "\n"

            if len(rule_findings) == 0:
                output += "  [SUCCESS] No findings\n"
            else:
                for finding in rule_findings:
                    output += self.format_finding(finding) + "\n"

            output += "\n"

        return output


Color = Literal["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
_SEVERITY_COLORS: dict[Severity, Color] = {
    Severity.ERROR: "red",
    Severity.FATAL: "red",
    Severity.WARNING: "yellow",
    Severity.INFO: "cyan",
}


def _color_severity(severity: Severity | Literal["SUCCESS"]) -> str:
    if severity == "SUCCESS":
        color = "green"
    else:
        color = _SEVERITY_COLORS[severity]
    return colored("[", "white") + colored(severity.upper(), color) + colored("]", "white")


class ColoringValidationFormatter(ValidationFormatter):
    def format_finding(self, finding: Finding) -> str:
        return f"  {_color_severity(finding.severity)} {finding.message()}"

    def format(self, findings: ValidationFindings[Context]) -> str:
        output = ""
        for rule, rule_findings in findings.items():
            meta = rule.metadata()
            name = meta.name

            output += colored("=" * len(name), "cyan") + "\n"
            output += colored(name, "white") + "\n"
            output += colored("=" * len(name), "cyan") + "\n"

            if meta.description is not None:
                output += "\n".join(wrap(meta.description)) + "\n"

            output += "\n"

            if len(rule_findings) == 0:
                output += f"  {_color_severity('SUCCESS')} No findings\n"
            else:
                for finding in rule_findings:
                    output += self.format_finding(finding) + "\n"

            output += "\n"

        return output
