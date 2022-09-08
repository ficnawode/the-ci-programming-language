from src.context import Context
from src.interpreter import Interpreter
from src.lexer import Lexer
from src.parser import Parser


def test_basic_arithmetic():
    test_cases = [
        ("2 plus 2", 4),
        ("2 minus 3", -1),
        ("2 minus plus 3", -1),
        ("2 minus minus 3", 5),
        ("10 do_potęgi 3", 1000),
        ("10 do_potęgi (minus 3)", 0.001),
        ("2 razy 8", 16),
        ("6 przez 3", 2),
        ("3 przez 6", 0.5),
    ]

    for input, output in test_cases:
        tokens, error = Lexer(input).lex()
        assert not error
        ast, error = Parser(tokens).parse()
        assert not error
        rt_result = Interpreter().visit(ast, Context("test"))
        assert not rt_result.error
        assert rt_result.value.value == output


def test_pemdas_arithmetic():
    test_cases = [
        ("2 plus 2 razy 3", 8),
        ("2 razy 2 plus 3", 7),
        ("2 minus 3 przez 3", 1),
        ("2 minus 3 do_potęgi 2", -7),
        ("minus 1 plus 3 przez minus 3", -2),
        ("3.5 razy 10 do_potęgi 3", 3500),
        ("minus 1 plus 10 do_potęgi (minus 3)", -0.999),
    ]

    for input, output in test_cases:
        tokens, error = Lexer(input).lex()
        assert not error
        ast, error = Parser(tokens).parse()
        assert not error
        rt_result = Interpreter().visit(ast, Context("test"))
        assert not rt_result.error
        assert rt_result.value.value == output
