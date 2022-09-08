from src.parser import Parser
from src.lexer import Lexer


def test_addition_and_subtraction():
    test_cases = [
        (
            "2 plus 2",
            "(INT:2, PLUS, INT:2)",
        ),
        (
            "2 plus 2 minus 2",
            "((INT:2, PLUS, INT:2), MINUS, INT:2)",
        ),
    ]

    for input, output in test_cases:
        tokens, error = Lexer(input).lex()
        assert not error
        # ast, error = Parser(tokens).parse()
        # assert not error
        # res = f"{ast}"
        # assert res == output


def test_multiplication_and_division():
    test_cases = [
        (
            "2 razy 2",
            "(INT:2, MUL, INT:2)",
        ),
        (
            "2 razy 2 przez 2",
            "((INT:2, MUL, INT:2), DIV, INT:2)",
        ),
    ]

    for input, output in test_cases:
        tokens, error = Lexer(input).lex()
        assert not error
        ast, error = Parser(tokens).parse()
        assert not error
        res = f"{ast}"
        assert res == output


def test_exponentials():
    test_cases = [
        (
            "2 do_potęgi 2",
            "(INT:2, POW, INT:2)",
        ),
        (
            "(2 do_potęgi 2) do_potęgi 0.5",
            "((INT:2, POW, INT:2), POW, FLOAT:0.5)",
        ),
    ]

    for input, output in test_cases:
        tokens, error = Lexer(input).lex()
        assert not error
        ast, error = Parser(tokens).parse()
        assert not error
        res = f"{ast}"
        assert res == output


def test_pemdas():
    test_cases = [
        (
            "2 plus 2 do_potęgi 2",
            "(INT:2, PLUS, (INT:2, POW, INT:2))",
        ),
        (
            "2 plus 2 razy 0.5",
            "(INT:2, PLUS, (INT:2, MUL, FLOAT:0.5))",
        ),
        (
            "(2 plus 2) do_potęgi 0.5",
            "((INT:2, PLUS, INT:2), POW, FLOAT:0.5)",
        ),
    ]

    for input, output in test_cases:
        tokens, error = Lexer(input).lex()
        assert not error
        ast, error = Parser(tokens).parse()
        assert not error
        res = f"{ast}"
        assert res == output
