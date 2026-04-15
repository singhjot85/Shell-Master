"""Formatter built on top of the compiler AST.

The formatter uses a small document tree so rendering stays linear and the
indentation depth is tracked explicitly instead of being inferred from strings.
That makes it much more suitable for larger jq programs than a plain join-based
renderer.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..compiler import (
    Accessor,
    AsExpression,
    ArrayExpression,
    BinaryExpression,
    CallExpression,
    ConditionalExpression,
    FunctionDefinition,
    Identifier,
    IndexExpression,
    JQCompiler,
    Literal,
    ObjectExpression,
    Program,
    ReduceExpression,
    UnaryExpression,
    Variable,
)
from .formatter_rules import FormatterRules


class Doc:
    """Base document node for the pretty-printer tree."""


@dataclass(slots=True)
class Text(Doc):
    value: str


@dataclass(slots=True)
class Line(Doc):
    indent_delta: int = 0


@dataclass(slots=True)
class AdjustIndent(Doc):
    delta: int


@dataclass(slots=True)
class Concat(Doc):
    parts: list[Doc]


def join_docs(parts: list[Doc], separator: Doc) -> Doc:
    """Join document nodes with a separator node."""

    if not parts:
        return Concat([])

    joined = [parts[0]]
    for part in parts[1:]:
        joined.extend([separator, part])
    return Concat(joined)


class JQFormatter:
    """Pretty-print supported jq AST nodes into stable multiline source."""

    def __init__(
        self,
        compiler: JQCompiler | None = None,
        rules: FormatterRules | None = None,
    ):
        self.compiler = compiler or JQCompiler()
        self.rules = rules or FormatterRules()

    def format(self, source: str) -> str:
        """Parse jq source and return a formatted string."""

        program = self.compiler.parse(source)
        return self.render_program(program)

    def render_program(self, program: Program) -> str:
        """Render a parsed jq program back into a formatted string."""

        return self._render_doc(self._build_program_doc(program)).rstrip()

    def _build_program_doc(self, program: Program) -> Doc:
        if not program.definitions:
            return self._build_expression_doc(program.expression)

        definition_docs = [self._build_definition_doc(definition) for definition in program.definitions]
        parts: list[Doc] = []
        for definition_doc in definition_docs:
            if parts:
                parts.extend([Line(), Line()])
            parts.append(definition_doc)
        parts.extend([Line(), Line(), self._build_expression_doc(program.expression)])
        return Concat(parts)

    def _build_expression_doc(self, expression) -> Doc:
        if isinstance(expression, Literal):
            return Text(self._format_literal(expression.value))
        if isinstance(expression, Identifier):
            return Text(expression.name)
        if isinstance(expression, Variable):
            return Text(f"${expression.name}")
        if isinstance(expression, Accessor):
            return Text(expression.path)
        if isinstance(expression, UnaryExpression):
            return Concat(
                [
                    Text(f"{expression.operator}{self.rules.space}"),
                    self._build_expression_doc(expression.operand),
                ]
            )
        if isinstance(expression, AsExpression):
            return self._build_as_doc(expression)
        if isinstance(expression, BinaryExpression):
            return self._build_binary_doc(expression)
        if isinstance(expression, CallExpression):
            return self._build_call_doc(expression)
        if isinstance(expression, IndexExpression):
            target = self._build_expression_doc(expression.target)
            suffix = "?" if expression.optional else ""
            if expression.index is None:
                return Concat([target, Text(f"[]{suffix}")])
            return Concat([target, Text("["), self._build_expression_doc(expression.index), Text(f"]{suffix}")])
        if isinstance(expression, ArrayExpression):
            return self._build_array_doc(expression)
        if isinstance(expression, ObjectExpression):
            return self._build_object_doc(expression)
        if isinstance(expression, ConditionalExpression):
            return self._build_conditional_doc(expression)
        if isinstance(expression, ReduceExpression):
            return self._build_reduce_doc(expression)
        raise TypeError(f"Unsupported expression type: {type(expression)!r}")

    def _build_definition_doc(self, definition: FunctionDefinition) -> Doc:
        signature = Text(f"def{self.rules.space}{definition.name}")
        if definition.parameters:
            parameter_docs = [Text(parameter) for parameter in definition.parameters]
            signature = Concat(
                [
                    signature,
                    Text("("),
                    join_docs(parameter_docs, Text(f";{self.rules.space}")),
                    Text(")"),
                ]
            )

        return Concat(
            [
                signature,
                Text(":"),
                AdjustIndent(1),
                Line(),
                self._build_expression_doc(definition.body),
                Text(";"),
                AdjustIndent(-1),
            ]
        )

    def _build_binary_doc(self, expression: BinaryExpression) -> Doc:
        if expression.operator == self.rules.pipe_operator and self.rules.multiline_pipelines:
            stages = self._flatten_binary(expression, "|")
            docs = [self._build_expression_doc(stage) for stage in stages]
            return join_docs(docs, Concat([Line(), Text(f"{self.rules.pipe_operator}{self.rules.space}")]))

        if expression.operator == self.rules.comma_operator:
            items = self._flatten_binary(expression, ",")
            docs = [self._build_expression_doc(item) for item in items]
            return join_docs(docs, Concat([Text(","), Line()]))

        return Concat(
            [
                self._build_expression_doc(expression.left),
                Text(f"{self.rules.space}{expression.operator}{self.rules.space}"),
                self._build_expression_doc(expression.right),
            ]
        )

    def _build_as_doc(self, expression: AsExpression) -> Doc:
        return Concat(
            [
                self._build_expression_doc(expression.source),
                Text(f"{self.rules.space}as{self.rules.space}{expression.variable}"),
                Line(),
                Text(f"{self.rules.pipe_operator}{self.rules.space}"),
                self._build_expression_doc(expression.body),
            ]
        )

    def _build_call_doc(self, expression: CallExpression) -> Doc:
        callee = self._build_expression_doc(expression.callee)
        if not expression.arguments:
            return Concat([callee, Text("()")])

        if self._is_compact_call(expression):
            arguments = [self._build_expression_doc(argument) for argument in expression.arguments]
            separator = Text(f"{self.rules.function_argument_separator}{self.rules.space}")
            return Concat([callee, Text("("), join_docs(arguments, separator), Text(")")])

        argument_docs = [self._build_expression_doc(argument) for argument in expression.arguments]
        return Concat(
            [
                callee,
                Text("("),
                Line(1),
                join_docs(
                    argument_docs,
                    Concat([Text(self.rules.function_argument_separator), Line()]),
                ),
                Line(-1),
                Text(")"),
            ]
        )

    def _build_array_doc(self, expression: ArrayExpression) -> Doc:
        if not expression.items:
            return Text(self.rules.empty_array)

        if self._is_compact_array(expression):
            item_docs = [self._build_expression_doc(item) for item in expression.items]
            return Concat([Text("["), join_docs(item_docs, Text(f",{self.rules.space}")), Text("]")])

        item_docs = [self._build_expression_doc(item) for item in expression.items]
        return Concat(
            [
                Text("["),
                Line(1),
                join_docs(item_docs, Concat([Text(","), Line()])),
                Line(-1),
                Text("]"),
            ]
        )

    def _build_object_doc(self, expression: ObjectExpression) -> Doc:
        if not expression.fields:
            return Text(self.rules.empty_object)

        if self._is_compact_object(expression):
            field_docs = [self._build_field_doc(field) for field in expression.fields]
            return Concat([Text("{"), join_docs(field_docs, Text(f",{self.rules.space}")), Text("}")])

        field_docs = [self._build_field_doc(field) for field in expression.fields]
        return Concat(
            [
                Text("{"),
                Line(1),
                join_docs(field_docs, Concat([Text(","), Line()])),
                Line(-1),
                Text("}"),
            ]
        )

    def _build_field_doc(self, field) -> Doc:
        if field.shorthand:
            return Text(field.key)
        return Concat([Text(f"{field.key}:{self.rules.space}"), self._build_expression_doc(field.value)])

    def _build_conditional_doc(self, expression: ConditionalExpression) -> Doc:
        if not self.rules.multiline_conditionals:
            return self._build_inline_conditional_doc(expression)

        parts: list[Doc] = []
        first = expression.branches[0]
        parts.extend(
            [
                Text(f"if{self.rules.space}"),
                self._build_expression_doc(first.condition),
                Text(f"{self.rules.space}then"),
                Line(1),
                self._build_expression_doc(first.body),
                Line(-1),
            ]
        )

        for branch in expression.branches[1:]:
            parts.extend(
                [
                    Text(f"elif{self.rules.space}"),
                    self._build_expression_doc(branch.condition),
                    Text(f"{self.rules.space}then"),
                    Line(1),
                    self._build_expression_doc(branch.body),
                    Line(-1),
                ]
            )

        if expression.fallback is not None:
            parts.extend([Text("else"), Line(1), self._build_expression_doc(expression.fallback), Line(-1)])

        parts.append(Text("end"))
        return Concat(parts)

    def _build_reduce_doc(self, expression: ReduceExpression) -> Doc:
        return Concat(
            [
                Text("reduce"),
                Text(self.rules.space),
                self._build_expression_doc(expression.source),
                Text(f"{self.rules.space}as{self.rules.space}{expression.variable}{self.rules.space}("),
                AdjustIndent(1),
                Line(),
                self._build_expression_doc(expression.initial),
                Text(self.rules.function_argument_separator),
                Line(),
                self._build_expression_doc(expression.update),
                AdjustIndent(-1),
                Line(),
                Text(")"),
            ]
        )

    def _render_doc(self, doc: Doc) -> str:
        pieces: list[str] = []
        self._emit(doc, depth=0, pieces=pieces)
        return "".join(pieces)

    def _emit(self, doc: Doc, depth: int, pieces: list[str]) -> int:
        if isinstance(doc, Text):
            pieces.append(doc.value)
            return depth
        if isinstance(doc, Line):
            next_depth = max(depth + doc.indent_delta, 0)
            pieces.append(self.rules.newline)
            pieces.append(self.rules.indent_unit * next_depth)
            return next_depth
        if isinstance(doc, AdjustIndent):
            return max(depth + doc.delta, 0)
        if isinstance(doc, Concat):
            current_depth = depth
            for part in doc.parts:
                current_depth = self._emit(part, current_depth, pieces)
            return current_depth
        raise TypeError(f"Unsupported doc node: {type(doc)!r}")

    def _flatten_binary(self, expression: BinaryExpression, operator: str) -> list:
        items = []

        def visit(node) -> None:
            if isinstance(node, BinaryExpression) and node.operator == operator:
                visit(node.left)
                visit(node.right)
                return
            items.append(node)

        visit(expression)
        return items

    def _is_compact_call(self, expression: CallExpression) -> bool:
        if not self.rules.multiline_calls:
            return True
        if len(expression.arguments) <= 1:
            return all(self._is_compact_expression(argument) for argument in expression.arguments)
        return len(expression.arguments) <= self.rules.compact_call_max_args and all(
            self._is_compact_expression(argument) for argument in expression.arguments
        )

    def _is_compact_array(self, expression: ArrayExpression) -> bool:
        if not self.rules.multiline_arrays:
            return True
        return len(expression.items) <= self.rules.compact_array_max_items and all(
            self._is_compact_expression(item) for item in expression.items
        )

    def _is_compact_object(self, expression: ObjectExpression) -> bool:
        if not self.rules.multiline_objects:
            return True
        return len(expression.fields) <= self.rules.compact_object_max_fields and all(
            field.shorthand or self._is_compact_expression(field.value) for field in expression.fields
        )

    def _is_compact_expression(self, expression) -> bool:
        return isinstance(expression, (Literal, Identifier, Variable, Accessor))

    def _format_literal(self, value) -> str:
        if value is None:
            return "null"
        if value is True:
            return "true"
        if value is False:
            return "false"
        return repr(value).replace("'", '"')

    def _build_inline_conditional_doc(self, expression: ConditionalExpression) -> Doc:
        parts: list[Doc] = []
        first = expression.branches[0]
        parts.extend(
            [
                Text(f"if{self.rules.space}"),
                self._build_expression_doc(first.condition),
                Text(f"{self.rules.space}then{self.rules.space}"),
                self._build_expression_doc(first.body),
            ]
        )
        for branch in expression.branches[1:]:
            parts.extend(
                [
                    Text(f"{self.rules.space}elif{self.rules.space}"),
                    self._build_expression_doc(branch.condition),
                    Text(f"{self.rules.space}then{self.rules.space}"),
                    self._build_expression_doc(branch.body),
                ]
            )
        if expression.fallback is not None:
            parts.extend(
                [
                    Text(f"{self.rules.space}else{self.rules.space}"),
                    self._build_expression_doc(expression.fallback),
                ]
            )
        parts.append(Text(f"{self.rules.space}end"))
        return Concat(parts)
