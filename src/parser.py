from src.node import NumberNode, UnaryOpNode, BinaryOpNode
from src.error import InvalidSyntaxError
import src.token_types as TT


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.token_id = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.token_id += 1
        if self.token_id < len(self.tokens):
            self.current_token = self.tokens[self.token_id]
        return self.current_token

    def parse(self):
        res = self.additive()
        if not res.error and self.current_token.type != TT.Abstract.EOF:
            res = res.failure(
                InvalidSyntaxError(
                    self.current_token.start,
                    self.current_token.end,
                    "Expected 'plus', 'minus', 'razy' 'przez' or 'do_potęgi'",
                )
            )
        return res.ast_root, res.error

    def literal(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (TT.Literals.INT, TT.Literals.FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(token))
        elif token.type == TT.Symbols.LPAREN:
            res.register(self.advance())
            expr = res.register(self.additive())
            if res.error:
                return res
            if self.current_token.type == TT.Symbols.RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_token.start,
                        self.current_token.end,
                        "Expected ')'",
                    )
                )

        return res.failure(
            InvalidSyntaxError(
                token.start,
                token.end,
                "Expected int, float, 'plus' or 'minus'",
            )
        )

    def power(self):
        return self.binary_operation(self.literal, (TT.Keywords.POW,))

    def unary(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (TT.Keywords.PLUS, TT.Keywords.MINUS):
            res.register(self.advance())
            factor = res.register(self.unary())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))

        return self.power()

    def multiplicative(self):
        return self.binary_operation(self.unary, (TT.Keywords.MUL, TT.Keywords.DIV))

    def additive(self):
        return self.binary_operation(
            self.multiplicative, (TT.Keywords.PLUS, TT.Keywords.MINUS)
        )

    def binary_operation(self, func_left, operators, func_right=None):
        if func_right == None:
            func_right = func_left

        res = ParseResult()
        left = res.register(func_left())
        if res.error:
            return res

        while self.current_token.type in operators:
            operator_token = self.current_token
            res.register(self.advance())
            right = res.register(func_right())
            if res.error:
                return res
            left = BinaryOpNode(left, operator_token, right)

        return res.success(left)


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
        self.ast_root = node
        return self

    def failure(self, error):
        self.error = error
        return self
