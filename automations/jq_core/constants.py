from enum import Enum
from dataclasses import dataclass


STRING_MAPPING= {
    '"':'"', 
    '\\':'\\', 
    '/':'/',
    'b':'\b', 
    'f':'\f', 
    'n':'\n', 
    'r':'\r', 
    't':'\t'
}

class TokenType(Enum):
    # Literals
    NULL = "NULL"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NUMBER = "NUMBER"
    STRING = "STRING"

    # Identifiers
    IDENTIFIER = "IDENTIFIER"
    VARIABLE = "VARIABLE"

    # Operators & punctuation
    DOT = "."
    COMMA = ","
    COLON = ":"
    PIPE = "|"

    PLUS = "+"
    MINUS = "-"
    MULT = "*"
    DIV = "/"
    MOD = "%"

    LT = "<"
    GT = ">"
    EQ = "=="
    NEQ = "!="
    LTE = "<="
    GTE = ">="
    ALT = "//"
    SLASH = '/'

    # Brackets
    LPAREN = "("
    RPAREN = ")"
    LSQRBRC = "["
    RSQRBRC = "]"
    LCURLBRC = "{"
    RCURLBRC= "}"

    # Keywords
    IF = "if"
    THEN = "then"
    ELSE = "else"
    ELIL= "elif"
    END = "end"

    AND = "and"
    OR = "or"
    NOT = "not"

    # Miscs
    EOF = "EOF"

KEYWORDS = {
    "if": TokenType.IF,
    "or": TokenType.OR,
    "end": TokenType.END,
    "and": TokenType.AND,
    "not": TokenType.NOT,
    "null": TokenType.NULL,
    "true": TokenType.TRUE,
    "then": TokenType.THEN,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
}

@dataclass
class Token:
    type: TokenType
    value: str | float | None
    line: int
    col: int

    def __repr__(self):
        return f"<Token {self.type}-{self.value}-[{self.line},{self.column}]>"