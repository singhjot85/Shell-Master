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
    IDENTIFIER = "IDENTIFIER" # firstName
    VARIABLE = "VARIABLE" # $firstName
    ACCESSOR_IDENTIFIER = "ACCESSOR_IDENTIFIER" # .firstName

    # Operators & punctuation
    DOT = "."
    COMMA = ","
    COLON = ":"
    PIPE = "|"
    DOLLAR = '$'

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
    ELIL = "elif"
    END = "end"

    AS = "as"

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

OPENING_BRACKETS = {
    str(TokenType.LPAREN.value): TokenType.LPAREN,
    str(TokenType.LSQRBRC.value): TokenType.LSQRBRC,
    str(TokenType.LCURLBRC.value): TokenType.LCURLBRC,
}

CLOSING_BRACKETS = {
    str(TokenType.RPAREN.value): TokenType.RPAREN,
    str(TokenType.RSQRBRC.value): TokenType.RSQRBRC,
    str(TokenType.RCURLBRC.value): TokenType.RCURLBRC,
}


KEYWORDS_MAPPING = {
    TokenType.AS.value: TokenType.AS,
    TokenType.OR.value: TokenType.OR,
    TokenType.AND.value: TokenType.AND,
    TokenType.NOT.value: TokenType.NOT,
    TokenType.IF.value: TokenType.IF,
    TokenType.ELSE.value: TokenType.ELSE,
    TokenType.ELIL.value: TokenType.ELIL,
    TokenType.THEN.value: TokenType.THEN,
    TokenType.END.value: TokenType.END,
    TokenType.NULL.value: TokenType.NULL,
    TokenType.TRUE.value: TokenType.TRUE,
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