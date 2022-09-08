from src.token import Token


class Node:
    def __init__(self, name: str) -> None:
        self.name = name


class NumberNode(Node):
    def __init__(self, token: Token):
        super().__init__("Literal")
        self.token = token
        self.start = token.start
        self.end = token.end

    def __repr__(self) -> str:
        return f"{self.token}"


class BinaryOpNode(Node):
    def __init__(self, left_node: Node, operator_token: Token, right_node: Node):
        super().__init__("Binary")
        self.left_node = left_node
        self.right_node = right_node
        self.operator_token = operator_token
        self.start = left_node.start
        self.end = right_node.end

    def __repr__(self) -> str:
        return f"({self.left_node}, {self.operator_token}, {self.right_node})"


class UnaryOpNode(Node):
    def __init__(self, operator_token: Token, node: Node):
        super().__init__("Unary")
        self.operator_token = operator_token
        self.node = node
        self.start = operator_token.start
        self.end = node.end

    def __repr__(self) -> str:
        return f"({self.operator_token}, {self.node})"
