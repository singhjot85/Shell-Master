"""Position-aware lexer for the jq compiler core."""

from __future__ import annotations

from decimal import Decimal

from .errors import LexerError
from .inputs import SourceReader
from .tokens import KEYWORDS, Token, TokenKind


class Lexer:
    """Turn jq source code into a stream of typed tokens."""

    def __init__(self, source: str | bytes | bytearray):
        self.reader = SourceReader(source)

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while self.reader.current is not None:
            char = self.reader.current
            if char in " \t\r\n":
                self.reader.advance()
                continue
            if char == "#":
                self._skip_comment()
                continue
            if char == '"':
                tokens.append(self._scan_string())
                continue
            if char == "$":
                tokens.append(self._scan_variable())
                continue
            if char == ".":
                tokens.append(self._scan_accessor())
                continue
            if char.isdigit() or (char == "-" and (self.reader.peek() or "").isdigit()):
                tokens.append(self._scan_number())
                continue
            if self._is_identifier_start(char):
                tokens.append(self._scan_identifier())
                continue
            tokens.append(self._scan_symbol())

        eof = self.reader.location()
        tokens.append(Token(TokenKind.EOF, "", None, eof, eof))
        return tokens

    def _skip_comment(self) -> None:
        while self.reader.current not in {None, "\n"}:
            self.reader.advance()

    def _scan_string(self) -> Token:
        start = self.reader.location()
        self.reader.advance()
        buffer: list[str] = []

        while self.reader.current is not None:
            char = self.reader.current
            if char == '"':
                self.reader.advance()
                return Token(
                    TokenKind.STRING,
                    f'"{"".join(buffer)}"',
                    "".join(buffer),
                    start,
                    self.reader.location(),
                )
            if char == "\\":
                self.reader.advance()
                escaped = self.reader.current
                if escaped is None:
                    raise LexerError("unterminated string escape", self.reader.location())
                buffer.append(self._decode_escape(escaped))
                self.reader.advance()
                continue
            if char == "\n":
                raise LexerError("newline inside string literal", self.reader.location())
            buffer.append(char)
            self.reader.advance()

        raise LexerError("unterminated string literal", start)

    def _decode_escape(self, escaped: str) -> str:
        mapping = {
            '"': '"',
            "\\": "\\",
            "/": "/",
            "b": "\b",
            "f": "\f",
            "n": "\n",
            "r": "\r",
            "t": "\t",
        }
        if escaped in mapping:
            return mapping[escaped]
        if escaped == "u":
            digits = []
            for _ in range(4):
                self.reader.advance()
                current = self.reader.current
                if current is None or current.lower() not in "0123456789abcdef":
                    raise LexerError("invalid unicode escape", self.reader.location())
                digits.append(current)
            return chr(int("".join(digits), 16))
        raise LexerError(f"unsupported escape sequence \\{escaped}", self.reader.location())

    def _scan_variable(self) -> Token:
        start = self.reader.location()
        self.reader.advance()
        if self.reader.current is None or not self._is_identifier_start(self.reader.current):
            raise LexerError("invalid variable name", start)
        name = self._consume_identifier_body()
        return Token(TokenKind.VARIABLE, f"${name}", name, start, self.reader.location())

    def _scan_accessor(self) -> Token:
        start = self.reader.location()
        self.reader.advance()
        buffer = ["."]

        current = self.reader.current
        if current == '"':
            string_token = self._scan_string()
            lexeme = f'.{string_token.lexeme}'
            return Token(TokenKind.ACCESSOR, lexeme, lexeme[1:], start, string_token.end)

        if current is not None and self._is_identifier_start(current):
            buffer.append(self._consume_identifier_body())

        lexeme = "".join(buffer)
        return Token(TokenKind.ACCESSOR, lexeme, lexeme[1:], start, self.reader.location())

    def _scan_number(self) -> Token:
        start = self.reader.location()
        buffer: list[str] = []

        if self.reader.current == "-":
            buffer.append("-")
            self.reader.advance()

        while (current := self.reader.current) is not None and current.isdigit():
            buffer.append(current)
            self.reader.advance()

        if self.reader.current == "." and (self.reader.peek() or "").isdigit():
            buffer.append(".")
            self.reader.advance()
            while (current := self.reader.current) is not None and current.isdigit():
                buffer.append(current)
                self.reader.advance()

        if (current := self.reader.current) is not None and current.lower() == "e":
            buffer.append(current)
            self.reader.advance()
            if self.reader.current in {"+", "-"}:
                buffer.append(self.reader.current)
                self.reader.advance()
            if self.reader.current is None or not self.reader.current.isdigit():
                raise LexerError("invalid exponent in number literal", self.reader.location())
            while (current := self.reader.current) is not None and current.isdigit():
                buffer.append(current)
                self.reader.advance()

        lexeme = "".join(buffer)
        if "e" in lexeme.lower():
            literal = Decimal(lexeme)
        elif "." in lexeme:
            literal = float(lexeme)
        else:
            literal = int(lexeme)
        return Token(TokenKind.NUMBER, lexeme, literal, start, self.reader.location())

    def _scan_identifier(self) -> Token:
        start = self.reader.location()
        name = self._consume_identifier_body()
        kind = KEYWORDS.get(name, TokenKind.IDENTIFIER)
        literal = None if kind is TokenKind.IDENTIFIER else name
        return Token(kind, name, literal, start, self.reader.location())

    def _scan_symbol(self) -> Token:
        start = self.reader.location()
        char = self.reader.current
        next_char = self.reader.peek() or ""
        pair = f"{char}{next_char}"

        paired_symbols = {
            "==": TokenKind.EQ,
            "!=": TokenKind.NE,
            "<=": TokenKind.LE,
            ">=": TokenKind.GE,
            "//": TokenKind.ALT,
        }
        single_symbols = {
            "(": TokenKind.LPAREN,
            ")": TokenKind.RPAREN,
            "[": TokenKind.LBRACKET,
            "]": TokenKind.RBRACKET,
            "{": TokenKind.LBRACE,
            "}": TokenKind.RBRACE,
            ",": TokenKind.COMMA,
            ":": TokenKind.COLON,
            ";": TokenKind.SEMICOLON,
            "|": TokenKind.PIPE,
            "?": TokenKind.QUESTION,
            "+": TokenKind.PLUS,
            "-": TokenKind.MINUS,
            "*": TokenKind.STAR,
            "/": TokenKind.SLASH,
            "%": TokenKind.PERCENT,
            "=": TokenKind.ASSIGN,
            "<": TokenKind.LT,
            ">": TokenKind.GT,
        }

        if pair in paired_symbols:
            self.reader.advance()
            self.reader.advance()
            return Token(paired_symbols[pair], pair, None, start, self.reader.location())
        if char in single_symbols:
            self.reader.advance()
            return Token(single_symbols[char], char, None, start, self.reader.location())
        raise LexerError(f"unexpected character {char!r}", start)

    def _consume_identifier_body(self) -> str:
        buffer: list[str] = []
        while (current := self.reader.current) is not None and self._is_identifier_part(current):
            buffer.append(current)
            self.reader.advance()
        return "".join(buffer)

    @staticmethod
    def _is_identifier_start(char: str) -> bool:
        return char.isalpha() or char == "_"

    @staticmethod
    def _is_identifier_part(char: str) -> bool:
        return char.isalnum() or char == "_"
