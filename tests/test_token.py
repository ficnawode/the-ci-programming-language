from src.token import Token_keywords


def test_enum_values():
    for token in Token_keywords:
        assert type(token.value) == str
