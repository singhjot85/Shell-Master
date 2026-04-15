"""Token definitions shared by the compiler and tooling layers."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .errors import SourceLocation


class TokenKind(str, Enum):
    EOF = "EOF"
    IDENTIFIER = "IDENTIFIER"
    ACCESSOR = "ACCESSOR"
    VARIABLE = "VARIABLE"
    NUMBER = "NUMBER"
    STRING = "STRING"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"
    IF = "IF"
    THEN = "THEN"
    ELIF = "ELIF"
    ELSE = "ELSE"
    END = "END"
    AS = "AS"
    DEF = "DEF"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    TRY = "TRY"
    CATCH = "CATCH"
    REDUCE = "REDUCE"
    FOREACH = "FOREACH"
    LABEL = "LABEL"
    BREAK = "BREAK"
    WHILE = "WHILE"
    UNTIL = "UNTIL"
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    LBRACE = "{"
    RBRACE = "}"
    COMMA = ","
    COLON = ":"
    SEMICOLON = ";"
    PIPE = "|"
    QUESTION = "?"
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    PERCENT = "%"
    ASSIGN = "="
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    ALT = "//"


KEYWORDS: dict[str, TokenKind] = {
    "if": TokenKind.IF,
    "then": TokenKind.THEN,
    "elif": TokenKind.ELIF,
    "else": TokenKind.ELSE,
    "end": TokenKind.END,
    "as": TokenKind.AS,
    "def": TokenKind.DEF,
    "and": TokenKind.AND,
    "or": TokenKind.OR,
    "not": TokenKind.NOT,
    "try": TokenKind.TRY,
    "catch": TokenKind.CATCH,
    "reduce": TokenKind.REDUCE,
    "foreach": TokenKind.FOREACH,
    "label": TokenKind.LABEL,
    "break": TokenKind.BREAK,
    "while": TokenKind.WHILE,
    "until": TokenKind.UNTIL,
    "true": TokenKind.TRUE,
    "false": TokenKind.FALSE,
    "null": TokenKind.NULL,
}


@dataclass(slots=True, frozen=True)
class Token:
    """A single lexeme and its source metadata."""

    kind: TokenKind
    lexeme: str
    literal: object | None
    start: SourceLocation
    end: SourceLocation
