from src.token import Token


class LiteralNode:
    def __init__(self, token: Token):
        self.token = token

    def __repr__(self) -> str:
        return f"{self.token}"


class BinaryOpNode:
    def __init__(self, left_node, operation_token: Token, right_node):
        self.left_node = left_node
        self.right_node = right_node
        self.operation_token = operation_token

    def __repr__(self) -> str:
        return f"({self.left_node}, {self.operation_token}, {self.right_node})"
