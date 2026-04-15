"""Debugger-style structural tracing for compiler output."""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass

from ..compiler import JQCompiler


@dataclass(slots=True)
class DebugTrace:
    """A simple structural trace of a compiled jq program."""

    token_summary: list[str] = field(default_factory=list)
    ast_summary: list[str] = field(default_factory=list)


class JQDebugger:
    """Produce human-readable compiler diagnostics without executing jq."""

    def __init__(self, compiler: JQCompiler | None = None):
        self.compiler = compiler or JQCompiler()

    def trace(self, source: str) -> DebugTrace:
        result = self.compiler.compile(source)
        return DebugTrace(
            token_summary=[f"{token.kind.value}: {token.lexeme}" for token in result.tokens],
            ast_summary=self._walk(result.ast),
        )

    def _walk(self, node, depth: int = 0) -> list[str]:
        indent = "  " * depth
        lines = [f"{indent}{type(node).__name__}"]
        if not is_dataclass(node):
            return lines
        for dataclass_field in fields(node):
            value = getattr(node, dataclass_field.name)
            if isinstance(value, list):
                for item in value:
                    if is_dataclass(item):
                        lines.extend(self._walk(item, depth + 1))
            elif is_dataclass(value):
                lines.extend(self._walk(value, depth + 1))
        return lines
