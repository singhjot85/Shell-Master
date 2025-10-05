from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    # Literals
    NULL = "null"
    TRUE = "true"
    FALSE = "false"
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
    SEMI_COLON = ";"
    PIPE = "|"
    DOLLAR = '$'
    ASTRICk = "*"

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
    QUESTION_MARK = '?'

    # Compound assignment (modifies field in place)
    PLUS_EQUL = "+="
    MINUS_EQUAL = "-=" 
    MULT_EQUAL = "*=" 
    DIV_EQUAL = "/="


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
    TRY = "try"
    CATCH = "catch"
    LABEL = "label"
    REDUCE = "reduce"
    FOREACH = "foreach"
    WHILE = "while"
    UNTIL = "until"
    BREAK = "break"
    
    DEF = "def"

    AS = "as"

    AND = "and"
    OR = "or"
    NOT = "not"

    # Miscs
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: str | float | None
    line: int
    col: int

    def __repr__(self):
        return f"<Token {self.type} - '{self.value}'>"

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

DEFAULT_IDENTIFIERS = {
    TokenType.IF.value: TokenType.IF,
    TokenType.THEN.value: TokenType.THEN,
    TokenType.ELIL.value: TokenType.ELIL,
    TokenType.ELSE.value: TokenType.ELSE,
    TokenType.END.value: TokenType.END,
    TokenType.AS.value: TokenType.AS,
    TokenType.AND.value: TokenType.AND,
    TokenType.OR.value: TokenType.OR,
    TokenType.NOT.value: TokenType.NOT,
    TokenType.NULL.value: TokenType.NULL,
    TokenType.TRY.value: TokenType.TRY,
    TokenType.CATCH.value: TokenType.CATCH,
    TokenType.LABEL.value: TokenType.LABEL,
    TokenType.REDUCE.value: TokenType.REDUCE,
    TokenType.FOREACH.value: TokenType.FOREACH,
    TokenType.WHILE.value: TokenType.WHILE,
    TokenType.UNTIL.value: TokenType.UNTIL, 
    TokenType.BREAK.value: TokenType.BREAK,
    TokenType.DEF.value: TokenType.DEF
}

OPERATORS = {
    TokenType.COLON.value: TokenType.COLON,
    TokenType.COMMA.value: TokenType.COMMA,
    TokenType.SEMI_COLON.value: TokenType.SEMI_COLON,
    TokenType.PIPE.value: TokenType.PIPE,
    TokenType.ASTRICk.value: TokenType.ASTRICk,
    TokenType.PLUS.value: TokenType.PLUS,
    TokenType.MINUS.value: TokenType.MINUS,
    TokenType.MULT.value: TokenType.MULT,
    TokenType.DIV.value: TokenType.DIV,
    TokenType.MOD.value: TokenType.MOD,
    TokenType.LT.value: TokenType.LT,
    TokenType.GT.value: TokenType.GT,
    TokenType.EQ.value: TokenType.EQ,
    TokenType.NEQ.value: TokenType.NEQ,
    TokenType.LTE.value: TokenType.LTE,
    TokenType.GTE.value: TokenType.GTE,
    TokenType.ALT.value: TokenType.ALT,
    TokenType.SLASH.value: TokenType.SLASH,
    TokenType.QUESTION_MARK.value: TokenType.QUESTION_MARK,
    TokenType.PLUS_EQUL.value: TokenType.PLUS_EQUL,
    TokenType.MINUS_EQUAL.value: TokenType.MINUS_EQUAL,
    TokenType.MULT_EQUAL.value: TokenType.MULT_EQUAL,
    TokenType.DIV_EQUAL.value: TokenType.DIV_EQUAL,
}