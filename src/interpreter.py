from __future__ import annotations
from src.number import Number
from src.node import BinaryOpNode, NumberNode, UnaryOpNode
from src.context import Context
from src.interpreter_result import InterpreterResult
import src.token_types as TT


class Interpreter:
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node: NumberNode, context: Context):
        return InterpreterResult().success(
            Number(node.token.value)
            .set_context(context)
            .set_position(node.start, node.end)
        )

    def visit_BinaryOpNode(self, node: BinaryOpNode, context: Context):
        interpreter_result = InterpreterResult()
        left = interpreter_result.register(self.visit(node.left_node, context))
        if interpreter_result.error:
            return interpreter_result
        right = interpreter_result.register(self.visit(node.right_node, context))
        if interpreter_result.error:
            return interpreter_result

        if node.operator_token.type == TT.Keywords.PLUS:
            result, error = left.added_to(right)
        elif node.operator_token.type == TT.Keywords.MINUS:
            result, error = left.subbed_by(right)
        elif node.operator_token.type == TT.Keywords.MUL:
            result, error = left.multed_by(right)
        elif node.operator_token.type == TT.Keywords.DIV:
            result, error = left.dived_by(right)
        elif node.operator_token.type == TT.Keywords.POW:
            result, error = left.powed_by(right)

        if error:
            return interpreter_result.failure(error)
        else:
            return interpreter_result.success(result.set_position(node.start, node.end))

    def visit_UnaryOpNode(self, node: UnaryOpNode, context: Context):
        result = InterpreterResult()
        number = result.register(self.visit(node.node, context))
        if result.error:
            return result

        error = None

        if node.operator_token.type == TT.Keywords.MINUS:
            number, error = number.multed_by(Number(-1))

        if error:
            return result.failure(error)
        else:
            return result.success(number.set_position(node.start, node.end))
