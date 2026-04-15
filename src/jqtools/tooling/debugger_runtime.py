"""Runtime adapter seam for jq debugging.

The goal is to keep the debugger tooling stable while allowing different
execution backends later, such as:

- a native Python jq evaluator
- a subprocess-backed jq runtime
- a VS Code language service bridge
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from .debugger_models import DebugMode


@dataclass(slots=True)
class RuntimeTraceEvent:
    """Raw runtime event emitted by a debugger backend."""

    phase: str
    node_id: int | None = None
    input_value: Any | None = None
    variables: dict[str, Any] = field(default_factory=dict)
    note: str | None = None


@dataclass(slots=True)
class RuntimeFailure:
    """Raw runtime failure from a debugger backend."""

    message: str
    node_id: int | None = None
    cascading: bool = False
    input_value: Any | None = None
    variables: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RuntimeDebugResult:
    """Full runtime debugging result from an execution backend."""

    ok: bool
    events: list[RuntimeTraceEvent] = field(default_factory=list)
    failure: RuntimeFailure | None = None


class JQRuntimeDebugger(Protocol):
    """Protocol implemented by future jq execution backends."""

    def debug(self, source: str, input_data: Any, mode: DebugMode) -> RuntimeDebugResult:
        """Execute jq with debugger instrumentation."""


class NoopRuntimeDebugger:
    """Default adapter used until a real runtime debugger is implemented."""

    def debug(self, source: str, input_data: Any, mode: DebugMode) -> RuntimeDebugResult:
        return RuntimeDebugResult(ok=True)
