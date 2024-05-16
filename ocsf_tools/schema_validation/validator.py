
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional

Context = TypeVar("Context")

@dataclass
class Finding:
    message: Optional[str] = None

class Rule(Generic[Context]):

    def rule_name(self) -> str:
        raise NotImplementedError

    def validate(self, context: Context) -> list[Finding]:
        raise NotImplementedError


class Validator(Generic[Context]):

    def __init__(self, context: Context):
        self.context = context

