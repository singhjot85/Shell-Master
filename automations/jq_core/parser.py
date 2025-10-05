from . import Token, TokenType, ParseError
from automations.jq_core.ast import *

class BaseParser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.total_tokens = len(tokens)
        self.current: Token = (self.tokens[0] or None)
        self.current_idx = 0
    
    def parse(self):
        """ Main entry point - returns a complete AST(Abstract Syntax Tree) """
        try:
            expr = self.parse_expression()
            # self.consume(TokenType.EOF, "Expected end of expression")
            return expr
        except Exception as e:
            raise ParseError(msg=str(e))

    def peek(self):
        """Look at the next token without consuming it"""
        if self.is_at_end():
            return None
        return self.tokens[self.current_idx + 1]

    def previous(self):
        """Return the most recently consumed token."""
        return self.tokens[self.current_idx - 1]

    def is_at_end(self):
        """Check if we've reached EOF."""
        return (
            self.current_idx == self.total_tokens - 1 
            or self.current==TokenType.EOF
        )

    def advance(self):
        """Consume the current token and move to next."""
        if not self.is_at_end():
            self.current_idx += 1
            self.current = self.tokens[self.current_idx]
        else:
            raise Exception(msg="Cannot move traverse after last token")

    def check(self, token_type):
        """Check if current token matches a given type (without consuming)."""
        if not self.current:
            return False
        return self.current.type == token_type

    def match(self, *types):
        for t in types:
            return self.check(t)
        return False

    def match_and_consume(self, *types):
        """If current token matches one of the given types, consume it."""
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, token_type, message):
        """Require a specific token type; throw error if not present."""
        if self.check(token_type):
            return self.advance()
        raise Exception(f"{message} at line {self.current.line}")

class Parser(BaseParser):

    def parse_expression(self):
        return self.parse_primary()

    def parse_primary(self):

        if self.match(TokenType.NUMBER):
            return NumberLiteral(float(self.current.value))

        if self.match(TokenType.STRING):
            return StringLiteral(self.current.value)

        if self.match(TokenType.NULL):
            return NullLiteral()

        if self.match(TokenType.DOT):
            return Identity()

        # if self.match(TokenType.LCURLBRC):
        #     return self.parse_object()

        raise Exception(f"Unexpected token {self.current}")
