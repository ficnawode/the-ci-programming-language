from enum import Enum


class Literals(Enum):
    INT = "__int"
    FLOAT = "__float"


class Keywords(Enum):
    PLUS = "plus"
    MINUS = "minus"
    DIV = "przez"
    MUL = "razy"
    EQ = "równa_się"
    POW = "do_potęgi"


class Symbols(Enum):
    LPAREN = "("
    RPAREN = ")"
    DOT = "."


class Abstract(Enum):
    EOF = "__eof"
    IDENTIFIER = "__identifier"
