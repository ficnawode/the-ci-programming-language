from enum import Enum
from src.position import Position


class Token:
    def __init__(
        self,
        type: Enum,
        value=None,
        start: Position = None,
        end: Position = None,
    ):
        self.type = type
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        if self.value:
            return f"{self.type.name}:{self.value}"
        return f"{self.type.name}"
