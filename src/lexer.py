import re
from src.error import InvalidTokenError
from src.token import Token_keywords, Token_literals, Token, Token_symbols
from src.position import Position


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.tokens = []
        self.position = Position(0, 0, 1, "shell", text)

    def lex(self):
        tokens = []
        while len(self.text) > 0:
            if not self.find_next_token(tokens):
                pos_start, pos_end = self.parse_bs()

                return [], InvalidTokenError(
                    pos_start,
                    pos_end,
                    f"lexer error",
                )
        return tokens, None

    def find_next_token(self, tokens: list) -> bool:
        if self.skip_whitespace():
            return True
        if self.parse_keyword(tokens):
            return True
        if self.parse_symbol(tokens):
            return True
        if self.parse_float_literal(tokens):
            return True
        if self.parse_int_literal(tokens):
            return True
        return False

    def skip_whitespace(self) -> bool:
        while re.match(r"\A\s+", self.text):
            res = re.match(r"\A[ \t]+", self.text)
            if res:
                start, end = res.span()
                self.text = self.text[end:]
                self.position.advance(end, end)
            res = re.match(r"\A[\n\r]+", self.text)
            if res:
                start, end = res.span()
                self.text = self.text[end:]
                self.position.advance(end, 0, end)
        if len(self.text) == 0:
            return True
        return False

    def parse_keyword(self, tokens: list) -> bool:
        for type in Token_keywords:
            pattern = r"\A" + re.escape(type.value) + r"(?![\w\d]+)"
            res = re.match(pattern, self.text)
            if res:
                start_pos = self.position.copy()
                start, end = res.span()
                self.position.advance(end, end)
                end_pos = self.position.copy()
                tokens.append(
                    Token(type, start_position=start_pos, end_position=end_pos)
                )
                start, end = res.span()
                self.text = self.text[end:]
                return True
        return False

    def parse_symbol(self, tokens: list) -> bool:
        for type in Token_symbols:
            pattern = r"\A" + re.escape(type.value)
            res = re.match(pattern, self.text)
            if res:
                start_pos = self.position.copy()
                start, end = res.span()
                self.position.advance(end, end)
                end_pos = self.position.copy()
                tokens.append(
                    Token(type, start_position=start_pos, end_position=end_pos)
                )
                start, end = res.span()
                self.text = self.text[end:]
                return True
        return False

    def parse_float_literal(self, tokens: list):
        pattern = r"\A(\d+\.\d*?)(?![\w\.])"
        res = re.match(pattern, self.text)
        if res:
            tokens.append(self.make_float(res))
            return True
        return False

    def parse_int_literal(self, tokens: list):
        pattern = r"\A(\d+?)(?![\w\.])"
        res = re.match(pattern, self.text)
        if res:
            tokens.append(self.make_int(res))
            return True
        return False

    def make_float(self, literal: re.Match) -> Token:
        start_pos = self.position.copy()
        start, end = literal.span()
        self.position.advance(end, end)
        end_pos = self.position.copy()
        type = Token_literals.FLOAT
        value = float(self.text[start:end])
        self.text = self.text[end:]
        return Token(type, value, start_pos, end_pos)

    def make_int(self, literal: re.Match) -> Token:
        start_pos = self.position.copy()
        start, end = literal.span()
        self.position.advance(end, end)
        end_pos = self.position.copy()
        type = Token_literals.INT
        value = int(self.text[start:end])
        self.text = self.text[end:]
        return Token(type, value, start_pos, end_pos)

    def parse_bs(self) -> tuple:
        res = re.match(r"\A\S+", self.text)
        pos_start = self.position.copy()
        start, end = res.span()
        self.position.advance(end, end)
        pos_end = self.position.copy()
        return (pos_start, pos_end)
