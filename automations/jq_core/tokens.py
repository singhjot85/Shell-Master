from enum import Enum
from dataclasses import dataclass


class TokenType(Enum):
    """Base for defining tokens
    Token Types:
    Keyword: Reserved words with fixed meaning in the language. Ex: if, else, try, etc.
    Identifiers: Names created by the programmer. Ex: variable names, function names
    Literals: Constant values. Ex: 10, "hello", true, null
    Operators: Symbols that perform computation. Ex: +, -, *, /
    Delimiters: Characters used to structure code. Ex: (, ), {, }, [, ], , ;, .
    """
    pass

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

class Identifiers(TokenType):
    ACCESS_VARIABLE = "access_variable"  # .first_name
    VARIAVBLE = "variable" # $firstName
    FUNCTION = "function"  # def fisrName: 

class Literals(TokenType):
    NUMBER = "number"      # 10 
    STRING = "string"      # "first Name"
    NULL = "null"
    TRUE = "true"
    FALSE = "false"

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

class Delimiters(TokenType):
    EOF = "EOF"
    DOT = "."
    PIPE = "|"
    HASH = "#"
    COMMA = ","
    COLON = ":"
    DOLLAR = '$'
    ASTRICk = "*"
    ALTERNATE = "//"
    BACK_SLASH = '/'
    SEMI_COLON = ";"
    DOUBLE_QOUTES = '"'
    QUESTION_MARK = '?'
    OPEN_PARENTHESIS = "("
    CLOSE_PARENTHESIS = ")"
    OPEN_CURLY_BRAKET = "{"
    CLOSE_CURLY_BRAKET = "}"
    OPEN_SQUARE_BRACKET = "["
    CLOSE_SQUARE_BRACKET = "]"

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

    def __repr__(self):
        return f"<Token {self.type} - '{self.value}'>"