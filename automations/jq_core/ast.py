from dataclasses import dataclass
from typing import Any, List, Optional

# Base node for common logic and type convention
@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    pass



# Basic Nodes
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
    name: str

@dataclass
class Identity(ASTNode):
    """Represents '.' in jq."""
    pass



# Expressions
@dataclass
class BinaryExpr(ASTNode):
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
    key: str
    value: ASTNode

@dataclass
class ObjectLiteral(ASTNode):
    pairs: List[Pair]

@dataclass
class ArrayLiteral(ASTNode):
    elements: List[ASTNode]


