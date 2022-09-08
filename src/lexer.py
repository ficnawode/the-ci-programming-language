from src.error import InvalidTokenError
from src.token import Token
import src.token_types as TT
import re
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
        tokens.append(Token(TT.Abstract.EOF, None, self.position, self.position))
        return tokens, None

    def find_next_token(self, tokens: list) -> bool:
        if self.skip_whitespace():
            print("whitespace")
            return True
        elif self.parse_keyword(tokens):
            print("keyword")
            return True
        elif self.parse_symbol(tokens):
            print("symbol")
            return True
        elif self.parse_float_literal(tokens):
            print("float")
            return True
        elif self.parse_int_literal(tokens):
            print("int")
            return True
        elif self.parse_identifier(tokens):
            print("identifier")
            return True
        else:
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
        for type in TT.Keywords:
            pattern = r"\A" + re.escape(type.value) + r"(?![\w\d]+)"
            res = re.match(pattern, self.text)
            if res:
                start_pos = self.position.copy()
                start, end = res.span()
                self.position.advance(end, end)
                end_pos = self.position.copy()
                tokens.append(Token(type, start=start_pos, end=end_pos))
                start, end = res.span()
                self.text = self.text[end:]
                return True
        return False

    def parse_symbol(self, tokens: list) -> bool:
        for type in TT.Symbols:
            pattern = r"\A" + re.escape(type.value)
            res = re.match(pattern, self.text)
            if res:
                start_pos = self.position.copy()
                start, end = res.span()
                self.position.advance(end, end)
                end_pos = self.position.copy()
                tokens.append(Token(type, start=start_pos, end=end_pos))
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

    def parse_identifier(self, tokens: list):
        pattern = r"\A(\w+?)+"
        res = re.match(pattern, self.text)
        if res:
            tokens.append(self.make_identifier(res))
            return True
        return False

    def make_identifier(self, literal: re.Match) -> Token:
        start, end = literal.span()
        start_pos = self.position.copy()
        self.position.advance(end, end)
        end_pos = self.position.copy()

        type = TT.Abstract.IDENTIFIER
        value = self.text[start:end]
        self.text = self.text[end:]
        return Token(type, value, start_pos, end_pos)

    def make_float(self, literal: re.Match) -> Token:
        start, end = literal.span()
        start_pos = self.position.copy()
        self.position.advance(end, end)
        end_pos = self.position.copy()

        type = TT.Literals.FLOAT
        value = float(self.text[start:end])
        self.text = self.text[end:]
        return Token(type, value, start_pos, end_pos)

    def make_int(self, literal: re.Match) -> Token:
        start_pos = self.position.copy()
        start, end = literal.span()
        self.position.advance(end, end)
        end_pos = self.position.copy()

        type = TT.Literals.INT
        value = int(self.text[start:end])
        self.text = self.text[end:]
        return Token(type, value, start_pos, end_pos)

    def parse_bs(self) -> tuple:
        res = re.match(r"\A(\S?)+", self.text)
        pos_start = self.position.copy()
        start, end = res.span()
        self.position.advance(end, end)
        pos_end = self.position.copy()
        return (pos_start, pos_end)
