"""Service helpers for jq debugger endpoints."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any

from jqtools import DebugMode, JQDebugger


@dataclass(slots=True)
class DebuggerResult:
    """Result of a debugger request."""

    payload: dict[str, Any]
    status_code: int


class JQDebuggerService:
    """Thin service wrapper around the jq debugger."""

    def __init__(self, debugger: JQDebugger | None = None):
        self.debugger = debugger or JQDebugger()

    def debug_jq(self, source: str, input_payload: str | None, mode: str) -> DebuggerResult:
        """Debug jq source and return a JSON-friendly payload."""

        debug_mode = DebugMode.DETAILED if mode == DebugMode.DETAILED.value else DebugMode.FAILURE_ONLY

        try:
            input_data = self._parse_input_payload(input_payload)
        except ValueError as exc:
            return DebuggerResult(
                status_code=400,
                payload={
                    "ok": False,
                    "mode": debug_mode.value,
                    "failure": {
                        "message": str(exc),
                        "snippet": None,
                        "cascading": False,
                        "input_context": None,
                        "execution_trace": [],
                    },
                    "frames": [],
                    "token_summary": [],
                    "ast_summary": [],
                },
            )

        report = self.debugger.debug(source, input_data=input_data, mode=debug_mode)
        payload = asdict(report)
        payload["mode"] = report.mode.value
        return DebuggerResult(status_code=200 if report.ok else 400, payload=payload)

    def _parse_input_payload(self, input_payload: str | None) -> Any | None:
        if input_payload is None:
            return None
        stripped = input_payload.strip()
        if not stripped:
            return None
        try:
            return json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Input JSON is invalid: {exc.msg} at line {exc.lineno}, column {exc.colno}") from exc
