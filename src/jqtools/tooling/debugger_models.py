"""Structured debugger models shared by UIs and future integrations."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DebugMode(str, Enum):
    """Supported debugger execution modes."""

    FAILURE_ONLY = "failure_only"
    DETAILED = "detailed"


@dataclass(slots=True)
class SourceSnippet:
    """A source snippet tied to a concrete span."""

    expression: str
    line: int
    column: int
    end_line: int
    end_column: int
    source_line: str


@dataclass(slots=True)
class RuntimeContextSnapshot:
    """Runtime data visible at a trace point."""

    input_value: Any | None = None
    variables: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ExecutionFrame:
    """A single execution step in the debugger trace."""

    phase: str
    snippet: SourceSnippet
    input_context: RuntimeContextSnapshot | None = None
    note: str | None = None


@dataclass(slots=True)
class DebugFailure:
    """Structured debugger failure information."""

    message: str
    snippet: SourceSnippet
    cascading: bool = False
    input_context: RuntimeContextSnapshot | None = None
    execution_trace: list[ExecutionFrame] = field(default_factory=list)


@dataclass(slots=True)
class DebugReport:
    """Debugger output consumed by APIs, UIs, and editor tooling."""

    mode: DebugMode
    ok: bool
    token_summary: list[str] = field(default_factory=list)
    ast_summary: list[str] = field(default_factory=list)
    frames: list[ExecutionFrame] = field(default_factory=list)
    failure: DebugFailure | None = None
