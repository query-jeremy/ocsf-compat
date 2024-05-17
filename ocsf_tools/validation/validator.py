from dataclasses import dataclass
from enum import StrEnum
from typing import TypeVar, Generic

Context = TypeVar("Context")


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    FATAL = "fatal"


class Finding:
    def message(self) -> str:
        raise NotImplementedError()


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
    def __init__(self, context: Context):
        self.context = context

    def rules(self) -> list[Rule[Context]]:
        raise NotImplementedError()

    def validate(self) -> ValidationFindings[Context]:
        findings: ValidationFindings[Context] = {}
        for rule in self.rules():
            findings[rule] = rule.validate(self.context)

        return findings

