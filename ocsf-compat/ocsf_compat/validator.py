
from typing import TypeVar, Generic

Context = TypeVar("Context")
Options = TypeVar("Options")


Message = tuple[str, str]

class ValidationRule(Generic[Context, Options]):

    def rule_name(self) -> str:
        raise NotImplementedError

    def validate(self, context: Context, options: Options) -> list[Message]:
        raise NotImplementedError


class Validator(Generic[Context, Options]):

    def __init__(self, context: Context, options: Options):
        self.context = context
        self.options = options

