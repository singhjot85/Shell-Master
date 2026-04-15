"""Pratt parser for the jq compiler core."""

from __future__ import annotations

from .ast import (
    Accessor,
    AsExpression,
    ArrayExpression,
    BinaryExpression,
    CallExpression,
    ConditionalBranch,
    ConditionalExpression,
    FunctionDefinition,
    Identifier,
    IndexExpression,
    Literal,
    ObjectExpression,
    ObjectField,
    Program,
    ReduceExpression,
    Span,
    UnaryExpression,
    Variable,
)
from .errors import ParserError
from .tokens import Token, TokenKind


PRECEDENCE: dict[TokenKind, int] = {
    TokenKind.COMMA: 5,
    TokenKind.AS: 8,
    TokenKind.PIPE: 10,
    TokenKind.OR: 20,
    TokenKind.AND: 30,
    TokenKind.EQ: 40,
    TokenKind.NE: 40,
    TokenKind.LT: 50,
    TokenKind.LE: 50,
    TokenKind.GT: 50,
    TokenKind.GE: 50,
    TokenKind.ALT: 55,
    TokenKind.PLUS: 60,
    TokenKind.MINUS: 60,
    TokenKind.STAR: 70,
    TokenKind.SLASH: 70,
    TokenKind.PERCENT: 70,
    TokenKind.LPAREN: 90,
    TokenKind.LBRACKET: 90,
    TokenKind.QUESTION: 90,
}


class Parser:
    """Top-down Pratt parser for a practical jq subset."""

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        definitions: list[FunctionDefinition] = []
        while self.check(TokenKind.DEF):
            definitions.append(self.parse_definition())

        expression = self.parse_expression()
        self.consume(TokenKind.EOF, "expected end of input")
        start = definitions[0].span.start if definitions else expression.span.start
        return Program(span=Span(start, expression.span.end), definitions=definitions, expression=expression)

    def parse_expression(self, precedence: int = 0):
        token = self.advance()
        left = self.nud(token)
        while precedence < self.get_precedence(self.peek().kind):
            token = self.advance()
            left = self.led(token, left)
        return left

    def nud(self, token: Token):
        if token.kind is TokenKind.NUMBER:
            return Literal(span=Span(token.start, token.end), value=token.literal)
        if token.kind is TokenKind.STRING:
            return Literal(span=Span(token.start, token.end), value=token.literal)
        if token.kind is TokenKind.TRUE:
            return Literal(span=Span(token.start, token.end), value=True)
        if token.kind is TokenKind.FALSE:
            return Literal(span=Span(token.start, token.end), value=False)
        if token.kind is TokenKind.NULL:
            return Literal(span=Span(token.start, token.end), value=None)
        if token.kind is TokenKind.IDENTIFIER:
            return Identifier(span=Span(token.start, token.end), name=token.lexeme)
        if token.kind is TokenKind.VARIABLE:
            return Variable(span=Span(token.start, token.end), name=token.literal)
        if token.kind is TokenKind.ACCESSOR:
            return Accessor(span=Span(token.start, token.end), path=token.lexeme)
        if token.kind in {TokenKind.MINUS, TokenKind.NOT}:
            operand = self.parse_expression(80)
            return UnaryExpression(span=Span(token.start, operand.span.end), operator=token.lexeme, operand=operand)
        if token.kind is TokenKind.LPAREN:
            expression = self.parse_expression()
            closing = self.consume(TokenKind.RPAREN, "expected ')' after grouped expression")
            expression.span = Span(token.start, closing.end)
            return expression
        if token.kind is TokenKind.LBRACKET:
            return self.parse_array(token)
        if token.kind is TokenKind.LBRACE:
            return self.parse_object(token)
        if token.kind is TokenKind.IF:
            return self.parse_if_expression(token)
        if token.kind is TokenKind.REDUCE:
            return self.parse_reduce_expression(token)
        raise ParserError(f"unexpected token {token.kind.value}", token.start)

    def led(self, token: Token, left):
        if token.kind in {
            TokenKind.COMMA,
            TokenKind.PIPE,
            TokenKind.OR,
            TokenKind.AND,
            TokenKind.EQ,
            TokenKind.NE,
            TokenKind.LT,
            TokenKind.LE,
            TokenKind.GT,
            TokenKind.GE,
            TokenKind.ALT,
            TokenKind.PLUS,
            TokenKind.MINUS,
            TokenKind.STAR,
            TokenKind.SLASH,
            TokenKind.PERCENT,
        }:
            right = self.parse_expression(PRECEDENCE[token.kind])
            return BinaryExpression(
                span=Span(left.span.start, right.span.end),
                left=left,
                operator=token.lexeme,
                right=right,
            )

        if token.kind is TokenKind.AS:
            variable = self.consume(TokenKind.VARIABLE, "expected variable after 'as'")
            self.consume(TokenKind.PIPE, "expected '|' after jq binding variable")
            body = self.parse_expression(PRECEDENCE[TokenKind.AS])
            return AsExpression(
                span=Span(left.span.start, body.span.end),
                source=left,
                variable=variable.lexeme,
                body=body,
            )

        if token.kind is TokenKind.LPAREN:
            arguments = []
            if not self.check(TokenKind.RPAREN):
                while True:
                    arguments.append(self.parse_expression(PRECEDENCE[TokenKind.COMMA]))
                    if not self.match(TokenKind.COMMA, TokenKind.SEMICOLON):
                        break
            closing = self.consume(TokenKind.RPAREN, "expected ')' after arguments")
            return CallExpression(span=Span(left.span.start, closing.end), callee=left, arguments=arguments)

        if token.kind is TokenKind.LBRACKET:
            index = None
            if not self.check(TokenKind.RBRACKET):
                index = self.parse_expression()
            closing = self.consume(TokenKind.RBRACKET, "expected ']' after index expression")
            optional = self.match(TokenKind.QUESTION)
            last = self.previous()
            return IndexExpression(
                span=Span(left.span.start, last.end),
                target=left,
                index=index,
                optional=optional,
            )

        if token.kind is TokenKind.QUESTION:
            return IndexExpression(span=Span(left.span.start, token.end), target=left, index=None, optional=True)

        raise ParserError(f"unexpected token {token.kind.value}", token.start)

    def parse_array(self, opening: Token) -> ArrayExpression:
        items = []
        if not self.check(TokenKind.RBRACKET):
            while True:
                items.append(self.parse_expression(PRECEDENCE[TokenKind.COMMA]))
                if not self.match(TokenKind.COMMA):
                    break
        closing = self.consume(TokenKind.RBRACKET, "expected ']' after array literal")
        return ArrayExpression(span=Span(opening.start, closing.end), items=items)

    def parse_object(self, opening: Token) -> ObjectExpression:
        fields: list[ObjectField] = []
        if not self.check(TokenKind.RBRACE):
            while True:
                key_token = self.advance()
                if key_token.kind not in {TokenKind.IDENTIFIER, TokenKind.STRING, TokenKind.ACCESSOR}:
                    raise ParserError("expected object field name", key_token.start)

                key = key_token.literal if key_token.kind is TokenKind.STRING else key_token.lexeme.lstrip(".")
                shorthand = True
                if self.match(TokenKind.COLON):
                    shorthand = False
                    value = self.parse_expression(PRECEDENCE[TokenKind.COMMA])
                else:
                    if key_token.kind is TokenKind.ACCESSOR:
                        value = Accessor(span=Span(key_token.start, key_token.end), path=key_token.lexeme)
                    else:
                        value = Identifier(span=Span(key_token.start, key_token.end), name=key_token.lexeme)

                fields.append(
                    ObjectField(
                        span=Span(key_token.start, value.span.end),
                        key=key,
                        value=value,
                        shorthand=shorthand,
                    )
                )
                if not self.match(TokenKind.COMMA):
                    break
        closing = self.consume(TokenKind.RBRACE, "expected '}' after object literal")
        return ObjectExpression(span=Span(opening.start, closing.end), fields=fields)

    def parse_if_expression(self, opening: Token) -> ConditionalExpression:
        branches = []
        condition = self.parse_expression()
        self.consume(TokenKind.THEN, "expected 'then' after if condition")
        body = self.parse_expression()
        branches.append(ConditionalBranch(span=Span(condition.span.start, body.span.end), condition=condition, body=body))

        while self.match(TokenKind.ELIF):
            branch_token = self.previous()
            condition = self.parse_expression()
            self.consume(TokenKind.THEN, "expected 'then' after elif condition")
            body = self.parse_expression()
            branches.append(
                ConditionalBranch(span=Span(branch_token.start, body.span.end), condition=condition, body=body)
            )

        fallback = None
        if self.match(TokenKind.ELSE):
            fallback = self.parse_expression()

        closing = self.consume(TokenKind.END, "expected 'end' after conditional")
        return ConditionalExpression(
            span=Span(opening.start, closing.end),
            branches=branches,
            fallback=fallback,
        )

    def parse_reduce_expression(self, opening: Token) -> ReduceExpression:
        """Parse jq reduce expressions."""

        source = self.parse_expression(PRECEDENCE[TokenKind.AS])
        self.consume(TokenKind.AS, "expected 'as' in reduce expression")
        variable = self.consume(TokenKind.VARIABLE, "expected reduce variable after 'as'")
        self.consume(TokenKind.LPAREN, "expected '(' after reduce variable")
        initial = self.parse_expression(PRECEDENCE[TokenKind.COMMA])
        self.consume(TokenKind.SEMICOLON, "expected ';' between reduce accumulator expressions")
        update = self.parse_expression(PRECEDENCE[TokenKind.COMMA])
        closing = self.consume(TokenKind.RPAREN, "expected ')' after reduce accumulator")
        return ReduceExpression(
            span=Span(opening.start, closing.end),
            source=source,
            variable=variable.lexeme,
            initial=initial,
            update=update,
        )

    def parse_definition(self) -> FunctionDefinition:
        """Parse a top-level jq function definition."""

        opening = self.consume(TokenKind.DEF, "expected 'def' at function definition start")
        name = self.consume(TokenKind.IDENTIFIER, "expected function name after 'def'")
        parameters: list[str] = []

        if self.match(TokenKind.LPAREN):
            if not self.check(TokenKind.RPAREN):
                while True:
                    parameter = self.consume(TokenKind.IDENTIFIER, "expected function parameter name")
                    parameters.append(parameter.lexeme)
                    if not self.match(TokenKind.SEMICOLON, TokenKind.COMMA):
                        break
            self.consume(TokenKind.RPAREN, "expected ')' after function parameter list")

        self.consume(TokenKind.COLON, "expected ':' after function signature")
        body = self.parse_expression()
        closing = self.consume(TokenKind.SEMICOLON, "expected ';' after function definition body")

        return FunctionDefinition(
            span=Span(opening.start, closing.end),
            name=name.lexeme,
            parameters=parameters,
            body=body,
        )

    def get_precedence(self, kind: TokenKind) -> int:
        return PRECEDENCE.get(kind, 0)

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        token = self.peek()
        self.current += 1
        return token

    def check(self, kind: TokenKind) -> bool:
        return self.peek().kind is kind

    def match(self, *kinds: TokenKind) -> bool:
        if self.peek().kind in kinds:
            self.current += 1
            return True
        return False

    def consume(self, kind: TokenKind, message: str) -> Token:
        if self.check(kind):
            return self.advance()
        raise ParserError(message, self.peek().start)
