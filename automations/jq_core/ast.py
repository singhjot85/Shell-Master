from dataclasses import dataclass
from typing import Any, List


# Base node for common logic and type convention
@dataclass
class ASTNode:
    """Base class for all AST nodes."""

    value: Any
    level: int
    children: list

    def __init__(self, value: Any, level: int):
        self.value: Any = value
        self.level: list = level
        self.children: list = []

    def add_children(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"ASTNode({self.value})"


"""
Primitive Nodes
Most probably will be Leaf nodes
"""


@dataclass
class NumberLiteral(ASTNode):
    value: float | int


@dataclass
class StringLiteral(ASTNode):
    value: str


@dataclass
class BooleanLiteral(ASTNode):
    value: bool


@dataclass
class NullLiteral(ASTNode):
    pass


@dataclass
class Identifier(ASTNode):
    """Identifier will have keywords as of now but later will be seperated,
    Ex: some_identifier
    """

    value: str


@dataclass
class Variable(ASTNode):
    """A JQ variable
    Format: $var
    """

    value: str


@dataclass
class Identity(ASTNode):
    """Represents '.' in jq
    this can be . or .some_val
    """

    value: Identifier | None


@dataclass
class BinaryExpr(ASTNode):
    """Binary expressions
    Ex: . * 2
    """

    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class PipeExpr(ASTNode):
    left: ASTNode
    right: ASTNode


@dataclass
class Grouping(ASTNode):
    expr: ASTNode


# Object and Array Nodes
@dataclass
class Pair(ASTNode):
    """To simplify Objects, an object will have multiple Pairs
    Ex: {... key: value, ...}
    last pair might not have comma, Ex: {.. key: value}
    """

    key: str
    value: ASTNode


@dataclass
class ObjectLiteral(ASTNode):
    pairs: List[Pair]


@dataclass
class ArrayLiteral(ASTNode):
    elements: List[ASTNode]
