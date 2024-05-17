from .validator import Finding, ValidationFindings, Context


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

            for finding in rule_findings:
                output += self.format_finding(finding) + "\n"

            output += "\n"

        return output
