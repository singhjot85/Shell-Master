from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    """Base for defining tokens
    Token Types:
    Keyword: Reserved words with fixed meaning in the language. Ex: if, else, try, etc.
    Identifiers: Names created by the programmer. Ex: variable names, function names
    Literals: Constant values. Ex: 10, "hello", true, null
    Operators: Symbols that perform computation. Ex: +, -, *, /
    Delimiters: Characters used to structure code. Ex: (, ), {, }, [, ], , ;, .
    """

    def __str__(self):
        return "TokenType"

    def __repr__(self):
        return "tokentype"


class Keywords(TokenType):
    IF = "if"
    AS = "as"
    OR = "or"
    END = "end"
    TRY = "try"
    DEF = "def"
    AND = "and"
    NOT = "not"
    THEN = "then"
    ELSE = "else"
    ELIL = "elif"
    CATCH = "catch"
    LABEL = "label"
    WHILE = "while"
    UNTIL = "until"
    BREAK = "break"
    REDUCE = "reduce"
    FOREACH = "foreach"

    def __str__(self):
        return "Keywords"

    def __repr__(self):
        return "keywords"


class Identifiers(TokenType):
    ACCESS_VARIABLE = "access_variable"  # .first_name
    MAPPING_KEY = "mapping_key"  # firstName:
    VARIAVBLE = "variable"  # $firstName
    FUNCTION = "function"  # def fisrName:

    def __str__(self):
        return "Identifiers"

    def __repr__(self):
        return "identifiers"


class Literals(TokenType):
    NUMBER = "number"  # 10
    STRING = "string"  # "first Name"
    NULL = "null"
    TRUE = "true"
    FALSE = "false"

    def __str__(self):
        return "Literals"

    def __repr__(self):
        return "literals"


class Operators(TokenType):
    ADDITION = "+"
    MODULUS = "%"
    DIVISION = "/"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    EQUALS = "=="
    LESS_THAN = "<"
    NOT_EQUAL = "!="
    ASSIGNMENT = "="
    GREATER_THAN = ">"
    LESS_THAN_EQUAL = "<="
    GREATER_THAN_EQUAL = ">="

    def __str__(self):
        return "Operators"

    def __repr__(self):
        return "operators"


class Delimiters(TokenType):
    EOF = "EOF"
    DOT = "."
    PIPE = "|"
    HASH = "#"
    COMMA = ","
    COLON = ":"
    DOLLAR = "$"
    ASTRICk = "*"
    ALTERNATE = "//"
    BACK_SLASH = "/"
    SEMI_COLON = ";"
    DOUBLE_QOUTES = '"'
    QUESTION_MARK = "?"
    OPEN_PARENTHESIS = "("
    CLOSE_PARENTHESIS = ")"
    OPEN_CURLY_BRAKET = "{"
    CLOSE_CURLY_BRAKET = "}"
    OPEN_SQUARE_BRACKET = "["
    CLOSE_SQUARE_BRACKET = "]"

    def __str__(self):
        return "Delimiters"

    def __repr__(self):
        return "delimiters"


@dataclass
class Token:
    """A Token for JQ program
    type (TokenType): Class Name of type of token.
    """

    category: str
    type: TokenType
    value: str | int | float | None
    line: int
    col: int

    def __str__(self):
        return f"<Token {self.type} - '{self.value}'>"

    def __repr__(self):
        return f"<Token {self.type} - '{self.value}'>"
