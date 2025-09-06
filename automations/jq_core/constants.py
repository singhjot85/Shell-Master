from enum import Enum
from dataclasses import dataclass

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
    ACCESSOR_IDENTIFIER = "ACCESSOR_IDENTIFIER"

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

WHITE_SPACES = [' ', '\t', '\r']
NEW_LINES = ['\n']
COMMENT_HASH = '#'
STRING_QUOTE = '"'

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

BRACKETS = {
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "[": TokenType.LSQRBRC,
    "]": TokenType.RSQRBRC,
    "{": TokenType.LCURLBRC,
    "}": TokenType.RCURLBRC,
}

KEYWORDS_MAPPING = {
    TokenType.IF.value: TokenType.IF,
    TokenType.OR.value: TokenType.OR,
    TokenType.END.value: TokenType.END,
    TokenType.AND.value: TokenType.AND,
    TokenType.NOT.value: TokenType.NOT,
    TokenType.NULL.value: TokenType.NULL,
    TokenType.TRUE.value: TokenType.TRUE,
    TokenType.THEN.value: TokenType.THEN,
    TokenType.ELSE.value: TokenType.ELSE,
    TokenType.FALSE.value: TokenType.FALSE
}

@dataclass
class Token:
    type: TokenType
    value: str | float | None
    line: int
    col: int

    def __repr__(self):
        return f"<Token {self.type} - '{self.value}'>"