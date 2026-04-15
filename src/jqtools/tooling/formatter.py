"""Formatter built on top of the compiler AST."""

from __future__ import annotations

from ..compiler import (
    Accessor,
    ArrayExpression,
    BinaryExpression,
    CallExpression,
    ConditionalExpression,
    Identifier,
    IndexExpression,
    JQCompiler,
    Literal,
    ObjectExpression,
    Program,
    UnaryExpression,
    Variable,
)


class JQFormatter:
    """Pretty-print the supported jq AST into stable, readable source."""

    def __init__(self, compiler: JQCompiler | None = None):
        self.compiler = compiler or JQCompiler()

    def format(self, source: str) -> str:
        program = self.compiler.parse(source)
        return self.render_program(program)

    def render_program(self, program: Program) -> str:
        return self.render_expression(program.expression)

    def render_expression(self, expression) -> str:
        if isinstance(expression, Literal):
            if expression.value is None:
                return "null"
            if expression.value is True:
                return "true"
            if expression.value is False:
                return "false"
            return repr(expression.value).replace("'", '"')
        if isinstance(expression, Identifier):
            return expression.name
        if isinstance(expression, Variable):
            return f"${expression.name}"
        if isinstance(expression, Accessor):
            return expression.path
        if isinstance(expression, UnaryExpression):
            return f"{expression.operator} {self.render_expression(expression.operand)}"
        if isinstance(expression, BinaryExpression):
            return (
                f"{self.render_expression(expression.left)} "
                f"{expression.operator} "
                f"{self.render_expression(expression.right)}"
            )
        if isinstance(expression, CallExpression):
            args = ", ".join(self.render_expression(argument) for argument in expression.arguments)
            return f"{self.render_expression(expression.callee)}({args})"
        if isinstance(expression, IndexExpression):
            suffix = "?" if expression.optional else ""
            if expression.index is None:
                return f"{self.render_expression(expression.target)}[]{suffix}"
            return f"{self.render_expression(expression.target)}[{self.render_expression(expression.index)}]{suffix}"
        if isinstance(expression, ArrayExpression):
            return f"[{', '.join(self.render_expression(item) for item in expression.items)}]"
        if isinstance(expression, ObjectExpression):
            rendered_fields = []
            for field in expression.fields:
                if field.shorthand:
                    rendered_fields.append(field.key)
                else:
                    rendered_fields.append(f"{field.key}: {self.render_expression(field.value)}")
            return f"{{{', '.join(rendered_fields)}}}"
        if isinstance(expression, ConditionalExpression):
            parts = []
            first = expression.branches[0]
            parts.append(
                f"if {self.render_expression(first.condition)} then {self.render_expression(first.body)}"
            )
            for branch in expression.branches[1:]:
                parts.append(
                    f"elif {self.render_expression(branch.condition)} then {self.render_expression(branch.body)}"
                )
            if expression.fallback is not None:
                parts.append(f"else {self.render_expression(expression.fallback)}")
            parts.append("end")
            return " ".join(parts)
        raise TypeError(f"Unsupported expression type: {type(expression)!r}")
