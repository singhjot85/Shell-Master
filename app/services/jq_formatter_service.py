"""Service helpers for jq formatting endpoints."""

from __future__ import annotations

from dataclasses import dataclass

from jqtools import JQFormatter
from jqtools.compiler import JQToolsError


@dataclass(slots=True)
class FormatterResult:
    """Result of a formatter request."""

    source: str
    formatted: str | None
    error: str | None = None

    @property
    def ok(self) -> bool:
        """Return whether the format operation succeeded."""

        return self.error is None


class JQFormatterService:
    """Thin service wrapper around the jq formatter core."""

    def __init__(self, formatter: JQFormatter | None = None):
        self.formatter = formatter or JQFormatter()

    def format_jq(self, source: str) -> FormatterResult:
        """Format jq source and capture any compiler errors."""

        try:
            return FormatterResult(source=source, formatted=self.formatter.format(source))
        except JQToolsError as exc:
            return FormatterResult(source=source, formatted=None, error=str(exc))
        except Exception as exc:
            return FormatterResult(source=source, formatted=None, error=f"Unexpected error: {exc}")
