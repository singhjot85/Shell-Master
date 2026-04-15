"""High-level compiler entrypoints used by tooling and user interfaces."""

from __future__ import annotations

from dataclasses import dataclass

from .ast import Program
from .lexer import Lexer
from .parser import Parser
from .tokens import Token


@dataclass(slots=True)
class CompilationResult:
    """Complete output of a compiler pass."""

    source: str
    tokens: list[Token]
    ast: Program


class JQCompiler:
    """Facade that exposes lexing and parsing as one coherent pipeline."""

    def tokenize(self, source: str | bytes | bytearray) -> list[Token]:
        return Lexer(source).tokenize()

    def parse(self, source: str | bytes | bytearray) -> Program:
        tokens = self.tokenize(source)
        return Parser(tokens).parse()

    def compile(self, source: str | bytes | bytearray) -> CompilationResult:
        text = source.decode("utf-8") if isinstance(source, (bytes, bytearray)) else source
        tokens = self.tokenize(text)
        ast = Parser(tokens).parse()
        return CompilationResult(source=text, tokens=tokens, ast=ast)
