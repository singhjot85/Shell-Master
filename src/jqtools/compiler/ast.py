"""Abstract syntax tree nodes for the jq compiler core."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .errors import SourceLocation


@dataclass(slots=True)
class Span:
    start: SourceLocation
    end: SourceLocation


@dataclass(slots=True)
class Node:
    span: Span


@dataclass(slots=True)
class Program(Node):
    expression: "Expression"
    definitions: list["FunctionDefinition"] = field(default_factory=list)


class Expression(Node):
    """Marker base class for expression nodes."""


@dataclass(slots=True)
class Identifier(Expression):
    name: str


@dataclass(slots=True)
class Variable(Expression):
    name: str


@dataclass(slots=True)
class Accessor(Expression):
    path: str


@dataclass(slots=True)
class Literal(Expression):
    value: Any


@dataclass(slots=True)
class UnaryExpression(Expression):
    operator: str
    operand: Expression


@dataclass(slots=True)
class BinaryExpression(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclass(slots=True)
class CallExpression(Expression):
    callee: Expression
    arguments: list[Expression] = field(default_factory=list)


@dataclass(slots=True)
class IndexExpression(Expression):
    target: Expression
    index: Expression | None
    optional: bool = False


@dataclass(slots=True)
class ArrayExpression(Expression):
    items: list[Expression] = field(default_factory=list)


@dataclass(slots=True)
class ObjectField(Node):
    key: str
    value: Expression
    shorthand: bool = False


@dataclass(slots=True)
class ObjectExpression(Expression):
    fields: list[ObjectField] = field(default_factory=list)


@dataclass(slots=True)
class ConditionalBranch(Node):
    condition: Expression
    body: Expression


@dataclass(slots=True)
class ConditionalExpression(Expression):
    branches: list[ConditionalBranch] = field(default_factory=list)
    fallback: Expression | None = None


@dataclass(slots=True)
class AsExpression(Expression):
    """A jq binding expression such as ``.[] as $item | ...``."""

    source: Expression
    variable: str
    body: Expression


@dataclass(slots=True)
class ReduceExpression(Expression):
    """A jq reduce expression."""

    source: Expression
    variable: str
    initial: Expression
    update: Expression


@dataclass(slots=True)
class FunctionDefinition(Node):
    """A top-level jq function definition."""

    name: str
    parameters: list[str] = field(default_factory=list)
    body: Expression | None = None
