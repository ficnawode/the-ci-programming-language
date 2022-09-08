from src.position import Position


class Error:
    def __init__(
        self, error_name: str, pos_start: Position, pos_end: Position, details: str
    ):
        self.error_name = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self) -> str:
        res = f"{self.error_name}: {self.details}\n"
        res += f"File {self.pos_start.filename}, line {self.pos_start.linenumber}"
        res += (
            "\n\t"
            + self.text_quote(self.pos_start.filetxt, self.pos_start, self.pos_end)
            + "\n"
        )
        return res

    @staticmethod
    def text_quote(text, pos_start, pos_end) -> str:
        return f"{text[pos_start.id : pos_end.id]}"


class InvalidTokenError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details: str):
        super().__init__("Invalid Token Error", pos_start, pos_end, details)
