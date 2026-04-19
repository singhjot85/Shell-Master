"""Structured debugger tooling for compiler and future runtime diagnostics."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any

from ..compiler import JQCompiler, JQToolsError, ParserError, Program
from ..compiler.ast import Node
from .debugger_models import DebugFailure, DebugMode, DebugReport, ExecutionFrame, RuntimeContextSnapshot
from .debugger_runtime import JQRuntimeDebugger, NoopRuntimeDebugger
from .debugger_source import NodeIndex, SourceMap


class JQDebugger:
    """Produce structured diagnostics that UIs and editors can consume."""

    def __init__(
        self,
        compiler: JQCompiler | None = None,
        runtime_debugger: JQRuntimeDebugger | None = None,
    ):
        self.compiler = compiler or JQCompiler()
        self.runtime_debugger = runtime_debugger or NoopRuntimeDebugger()

    def trace(self, source: str) -> DebugReport:
        """Backward-compatible structural trace for non-runtime inspection."""

        result = self.compiler.compile(source)
        return DebugReport(
            mode=DebugMode.FAILURE_ONLY,
            ok=True,
            token_summary=[f"{token.kind.value}: {token.lexeme}" for token in result.tokens],
            ast_summary=self._walk(result.ast),
        )

    def debug(
        self,
        source: str,
        input_data: Any | None = None,
        mode: DebugMode = DebugMode.FAILURE_ONLY,
    ) -> DebugReport:
        """Debug jq source in failure-only or detailed mode.

        Today this produces:
        - compiler/parser failures with exact source location and expression context
        - structured runtime-ready reports using the same output model

        Once a real jq runtime adapter is plugged in, the same method can enrich
        the report with execution-time frames and input snapshots without
        changing callers.
        """

        source_map = SourceMap(source)
        try:
            compilation = self.compiler.compile(source)
        except ParserError as exc:
            snippet = source_map.snippet_from_span(
                self._synthetic_span(exc.location.line, exc.location.column)
            )
            return DebugReport(
                mode=mode,
                ok=False,
                failure=DebugFailure(
                    message=exc.message,
                    snippet=snippet,
                    cascading=False,
                    execution_trace=[],
                ),
            )
        except JQToolsError as exc:
            location = getattr(exc, "location", None)
            line = location.line if location is not None else 1
            column = location.column if location is not None else 1
            snippet = source_map.snippet_from_span(self._synthetic_span(line, column))
            return DebugReport(
                mode=mode,
                ok=False,
                failure=DebugFailure(message=str(exc), snippet=snippet, cascading=False),
            )

        node_index = NodeIndex().build(compilation.ast)
        runtime = self.runtime_debugger.debug(source, input_data, mode)
        frames = self._build_frames(compilation.ast, source_map, node_index, runtime.events, mode)
        failure = self._build_runtime_failure(source_map, node_index, runtime.failure, frames, mode)

        return DebugReport(
            mode=mode,
            ok=runtime.ok and failure is None,
            token_summary=[f"{token.kind.value}: {token.lexeme}" for token in compilation.tokens],
            ast_summary=self._walk(compilation.ast),
            frames=frames if mode is DebugMode.DETAILED else [],
            failure=failure,
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

    def _build_frames(
        self,
        program: Program,
        source_map: SourceMap,
        node_index: NodeIndex,
        runtime_events,
        mode: DebugMode,
    ) -> list[ExecutionFrame]:
        if not runtime_events:
            return self._build_static_frames(program, source_map, mode)

        frames: list[ExecutionFrame] = []
        for event in runtime_events:
            node = node_index.get_node(event.node_id) or program.expression
            frame = ExecutionFrame(
                phase=event.phase,
                snippet=source_map.snippet_from_node(node),
                note=event.note,
            )
            if mode is DebugMode.DETAILED:
                frame.input_context = RuntimeContextSnapshot(
                    input_value=event.input_value,
                    variables=event.variables,
                )
            frames.append(frame)
        return frames

    def _build_static_frames(self, program: Program, source_map: SourceMap, mode: DebugMode) -> list[ExecutionFrame]:
        frames: list[ExecutionFrame] = []

        for definition in program.definitions:
            frames.append(
                ExecutionFrame(
                    phase="definition",
                    snippet=source_map.snippet_from_node(definition),
                    note=f"Function definition: {definition.name}",
                    input_context=RuntimeContextSnapshot() if mode is DebugMode.DETAILED else None,
                )
            )
        frames.append(
            ExecutionFrame(
                phase="expression",
                snippet=source_map.snippet_from_node(program.expression),
                note="Top-level jq expression",
                input_context=RuntimeContextSnapshot() if mode is DebugMode.DETAILED else None,
            )
        )
        return frames

    def _build_runtime_failure(
        self,
        source_map: SourceMap,
        node_index: NodeIndex,
        runtime_failure,
        frames: list[ExecutionFrame],
        mode: DebugMode,
    ) -> DebugFailure | None:
        if runtime_failure is None:
            return None

        node = node_index.get_node(runtime_failure.node_id)
        if node is None:
            snippet = source_map.snippet_from_span(self._synthetic_span(1, 1))
        else:
            snippet = source_map.snippet_from_node(node)

        return DebugFailure(
            message=runtime_failure.message,
            snippet=snippet,
            cascading=runtime_failure.cascading,
            input_context=(
                RuntimeContextSnapshot(
                    input_value=runtime_failure.input_value,
                    variables=runtime_failure.variables,
                )
                if mode is DebugMode.DETAILED
                else None
            ),
            execution_trace=frames,
        )

    def _synthetic_span(self, line: int, column: int):
        from ..compiler.ast import Span
        from ..compiler.errors import SourceLocation

        start = SourceLocation(line=line, column=column, offset=0)
        end = SourceLocation(line=line, column=column + 1, offset=0)
        return Span(start=start, end=end)
