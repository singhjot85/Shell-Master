"""Helpers for mapping AST spans back to readable source snippets."""

from __future__ import annotations

from dataclasses import fields, is_dataclass

from ..compiler.ast import Node, Span
from .debugger_models import SourceSnippet


class SourceMap:
    """Index source text for debugger reports and editor integrations."""

    def __init__(self, source: str):
        self.source = source
        self.lines = source.splitlines() or [source]

    def snippet_from_span(self, span: Span) -> SourceSnippet:
        """Build a structured snippet from a compiler span."""

        line_index = max(span.start.line - 1, 0)
        source_line = self.lines[line_index] if line_index < len(self.lines) else ""
        expression = self._slice_expression(span)
        return SourceSnippet(
            expression=expression,
            line=span.start.line,
            column=span.start.column,
            end_line=span.end.line,
            end_column=span.end.column,
            source_line=source_line,
        )

    def snippet_from_node(self, node: Node) -> SourceSnippet:
        """Build a snippet from an AST node."""

        return self.snippet_from_span(node.span)

    def _slice_expression(self, span: Span) -> str:
        if span.start.line == span.end.line:
            line_index = max(span.start.line - 1, 0)
            line = self.lines[line_index] if line_index < len(self.lines) else ""
            start = max(span.start.column - 1, 0)
            end = max(span.end.column - 1, start)
            return line[start:end].strip() or line.strip()

        selected = self.lines[max(span.start.line - 1, 0) : span.end.line]
        return "\n".join(selected).strip()


class NodeIndex:
    """Assign stable integer ids to AST nodes for runtime debugger backends."""

    def __init__(self):
        self._node_to_id: dict[int, int] = {}
        self._id_to_node: dict[int, Node] = {}
        self._next_id = 1

    def build(self, root: Node) -> "NodeIndex":
        self._visit(root)
        return self

    def get_id(self, node: Node) -> int | None:
        return self._node_to_id.get(id(node))

    def get_node(self, node_id: int | None) -> Node | None:
        if node_id is None:
            return None
        return self._id_to_node.get(node_id)

    def _visit(self, value) -> None:
        if isinstance(value, Node):
            node_id = self._node_to_id.setdefault(id(value), self._next_id)
            if node_id == self._next_id:
                self._id_to_node[node_id] = value
                self._next_id += 1

        if not is_dataclass(value):
            return

        for dataclass_field in fields(value):
            child = getattr(value, dataclass_field.name)
            if isinstance(child, list):
                for item in child:
                    self._visit(item)
            else:
                self._visit(child)
