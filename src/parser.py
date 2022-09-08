from src.token import Token, Token_literals, Token_keywords
from src.node import LiteralNode, BinaryOpNode


class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.token_id = -1
        self.advance()

    def advance(self) -> Token:
        self.token_id += 1
        if self.token_id < len(self.tokens):
            self.current_token = self.tokens[self.token_id]
        return self.current_token

    def literal(self):
        token = self.current_token
        if token.type in Token_literals:
            self.advance()
            return LiteralNode(token)

    def term(self):
        left = self.literal()
        while self.current_token in (Token_keywords.DIV, Token_keywords.MUL):
            operator_token = self.current_token
            right = self.literal()
            left = BinaryOpNode(left, operator_token, right)
        return left


class ParseResult:
    def __init__(self):
        self.error = None
        self.ast_root = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
                return res.ast_root
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
