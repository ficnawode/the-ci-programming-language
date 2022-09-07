from enum import Enum
from src.position import Position


class Token_literals(Enum):
    INT = "__int"
    FLOAT = "__float"


class Token_keywords(Enum):
    PLUS = "plus"
    MINUS = "minus"
    DIV = "przez"
    MUL = "razy"
    EQ = "równa_się"

class Token_symbols(Enum):
    LPAREN = "("
    RPAREN = ")"
    DOT = "."

class Token:
    def __init__(
        self,
        type: Enum,
        value=None,
        start_position: Position = None,
        end_position: Position = None,
    ):
        self.type = type
        self.value = value
        self.start_position = start_position
        end_position = end_position

    def __repr__(self) -> str:
        if self.value:
            return f"{self.type.name}:{self.value}"
        return f"{self.type.name}"
