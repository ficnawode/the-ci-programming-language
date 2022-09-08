from __future__ import annotations
from src.interpreter_result import InterpreterResult
from src.position import Position
from src.error import RuntimeError
from src.context import Context


class Number:
    def __init__(self, value):
        self.value = value
        self.set_position()
        self.set_context()

    def set_position(self, start: Position = None, end: Position = None):
        self.start = start
        self.end = end
        return self

    def set_context(self, context: Context = None):
        self.context = context
        return self

    def added_to(self, other: Number) -> InterpreterResult:
        return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other: Number) -> InterpreterResult:
        return Number(self.value - other.value).set_context(self.context), None

    def multed_by(self, other: Number) -> InterpreterResult:
        return Number(self.value * other.value).set_context(self.context), None

    def dived_by(self, other: Number) -> InterpreterResult:
        if other.value == 0:
            return None, RuntimeError(
                other.start, other.end, "Division by zero", self.context
            )
        return Number(self.value / other.value).set_context(self.context), None

    def powed_by(self, other: Number) -> InterpreterResult:
        return Number(self.value**other.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)
