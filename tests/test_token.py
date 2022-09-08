import src.token_types as TT


def test_enum_values():
    for token in TT.Keywords:
        assert type(token.value) == str
