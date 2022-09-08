from src.context import Context
from src.interpreter import Interpreter
from src.lexer import Lexer
from src.parser import Parser


class Shell:
    def __init__(self):
        self.show_debug_info = True

    def run(self) -> None:
        while 1:
            current_line = input(">")
            tokens, error = Lexer(current_line).lex()
            if self.show_debug_info:
                if error:
                    print(error)
                    continue
                else:
                    print(tokens)
            ast, error = Parser(tokens).parse()
            if self.show_debug_info:
                if error:
                    print(error)
                    continue
                else:
                    print(ast)

            interpreter_result = Interpreter().visit(ast, Context("shell"))
            if not interpreter_result.error:
                print(interpreter_result.value)
