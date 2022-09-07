from src.lexer import Lexer


class Shell:
    def __init__(self):
        self.current_line = ""
        self.show_debug_info = True

    def run(self) -> None:
        while 1:
            self.current_line = input(">")
            tokens, error = Lexer(self.current_line).lex()
            if self.show_debug_info:
                if error:
                    print(error)
                else:
                    print(tokens)
