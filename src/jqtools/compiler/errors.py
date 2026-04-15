"""Compiler-facing exception types for the jq tools project."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SourceLocation:
    """A 1-based position in the source program."""

    line: int
    column: int
    offset: int


class JQToolsError(Exception):
    """Base class for all project-specific errors."""


class LexerError(JQToolsError):
    """Raised when the lexer cannot produce a valid token stream."""

    def __init__(self, message: str, location: SourceLocation):
        self.message = message
        self.location = location
        super().__init__(f"Lexing failed at {location.line}:{location.column}: {message}")


class ParserError(JQToolsError):
    """Raised when a token stream cannot be parsed into an AST."""

    def __init__(self, message: str, location: SourceLocation):
        self.message = message
        self.location = location
        super().__init__(f"Parsing failed at {location.line}:{location.column}: {message}")
