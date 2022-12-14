from src.lexer import Lexer
from src.token import Token_keywords, Token_literals, Token_symbols


def test_all_tokens():
    for keyword in Token_keywords:
        tokens, error = Lexer(" \r " + keyword.value + " \n\t  ").lex()
        assert not error
        assert tokens[0].type.name == keyword.name


def test_float_token_positive():
    test_cases = ["0.5", "1.22", "12312321.2153452345", "123.2 plus", "1."]
    for test_case in test_cases:
        tokens, error = Lexer(test_case).lex()
        assert not error
        assert tokens[0].type.name == Token_literals.FLOAT.name


def test_float_token_negative():
    test_cases = ["1a", "123", "2.9h", "plus3.2", "1.0.1"]
    for test_case in test_cases:
        tokens, error = Lexer(test_case).lex()
        assert error or tokens[0].type.name != Token_literals.FLOAT.name


def test_int_token_positive():
    test_cases = ["5", "122", "12312321", "123 plus"]
    for test_case in test_cases:
        tokens, error = Lexer(test_case).lex()
        assert not error
        assert tokens[0].type.name == Token_literals.INT.name


def test_int_token_negative():
    test_cases = ["1B", "1.0.1", "1plus"]
    for test_case in test_cases:
        tokens, error = Lexer(test_case).lex()
        assert error or tokens[0].type.name != Token_literals.INT.name


def test_complex_case():
    test_cases = [
        (
            "((()))",
            [
                Token_symbols.LPAREN,
                Token_symbols.LPAREN,
                Token_symbols.LPAREN,
                Token_symbols.RPAREN,
                Token_symbols.RPAREN,
                Token_symbols.RPAREN,
            ],
        ),
        (
            "(10 plus 47.0 równa_się 57.0)",
            [
                Token_symbols.LPAREN,
                Token_literals.INT,
                Token_keywords.PLUS,
                Token_literals.FLOAT,
                Token_keywords.EQ,
                Token_literals.FLOAT,
                Token_symbols.RPAREN,
            ],
        ),
    ]
    for input, output in test_cases:
        tokens, error = Lexer(input).lex()
        assert not error
        assert [t.type for t in tokens] == output


def test_position():
    test_cases = [
        ("((()))", [6, 6, 1]),
        ("\n\n  ", [4, 2, 3]),
        ("\nplus\n  ", [8, 2, 3]),
        ("\n1234\n  ", [8, 2, 3]),
        ("\nplus 1234 \n  ", [14, 2, 3]),
        ("\nrówna_się\n  ", [13, 2, 3]),
        ("plus adfa", [9, 9, 1]),
    ]
    for input, output in test_cases:
        _lexer = Lexer(input)
        tokens, error = _lexer.lex()
        assert _lexer.position.id == output[0]
        assert _lexer.position.column == output[1]
        assert _lexer.position.linenumber == output[2]
