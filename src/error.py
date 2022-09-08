from src.position import Position
from src.context import Context


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
        res += f"File {self.pos_start.file_name}, line {self.pos_start.linenumber}"
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
        super().__init__("Lexer: Invalid Token Error", pos_start, pos_end, details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details: str = ""):
        super().__init__("Parser: Invalid Syntax Error", pos_start, pos_end, details)


class RuntimeError(Error):
    def __init__(
        self, pos_start: Position, pos_end: Position, details: str, context: Context
    ):
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context

    def __repr__(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}"
        result += "\n\t" + self.text_quote(
            self.pos_start.ftxt, self.pos_start, self.pos_end
        )
        return result

    def generate_traceback(self):
        result = ""
        position = self.pos_start
        context = self.context

        while context:
            result = (
                f"  File {position.file_name}, line {str(position.ln + 1)}, in {context.display_name}\n"
                + result
            )
            position = context.parent_entry_pos
            context = context.parent
        return "Traceback (most recent call last):\n" + result
