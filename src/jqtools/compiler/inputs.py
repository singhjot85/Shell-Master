"""Input primitives used by the lexer."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import SourceLocation


@dataclass(slots=True)
class InputCheckpoint:
    """A saved reader position that can be restored later."""

    index: int
    line: int
    column: int


class SourceReader:
    """Position-aware source reader used by the lexer."""

    def __init__(self, source: str | bytes | bytearray):
        if isinstance(source, (bytes, bytearray)):
            source = bytes(source).decode("utf-8")
        if not isinstance(source, str):
            raise TypeError("source must be str, bytes, or bytearray")

        self.text = source
        self.length = len(source)
        self.index = 0
        self.line = 1
        self.column = 1

    @property
    def current(self) -> str | None:
        if self.index >= self.length:
            return None
        return self.text[self.index]

    def peek(self, offset: int = 1) -> str | None:
        index = self.index + offset
        if index >= self.length:
            return None
        return self.text[index]

    def advance(self) -> str | None:
        char = self.current
        if char is None:
            return None

        self.index += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def location(self) -> SourceLocation:
        return SourceLocation(self.line, self.column, self.index)

    def mark(self) -> InputCheckpoint:
        return InputCheckpoint(self.index, self.line, self.column)

    def restore(self, checkpoint: InputCheckpoint) -> None:
        self.index = checkpoint.index
        self.line = checkpoint.line
        self.column = checkpoint.column
