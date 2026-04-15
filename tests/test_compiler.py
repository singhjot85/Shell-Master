"""High-level tests for the jq compiler core."""

from decimal import Decimal

from jqtools.compiler import (
    BinaryExpression,
    CallExpression,
    ConditionalExpression,
    IndexExpression,
    JQCompiler,
    Literal,
    ObjectExpression,
    TokenKind,
)


def test_lexer_emits_expected_token_kinds():
    tokens = JQCompiler().tokenize('.name | {greeting: "hi", count: 2}')
    assert [token.kind for token in tokens[:9]] == [
        TokenKind.ACCESSOR,
        TokenKind.PIPE,
        TokenKind.LBRACE,
        TokenKind.IDENTIFIER,
        TokenKind.COLON,
        TokenKind.STRING,
        TokenKind.COMMA,
        TokenKind.IDENTIFIER,
        TokenKind.COLON,
    ]


def test_parser_respects_operator_precedence():
    program = JQCompiler().parse("1 + 2 * 3")
    expression = program.expression
    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "+"
    assert isinstance(expression.right, BinaryExpression)
    assert expression.right.operator == "*"


def test_parser_builds_pipe_call_and_index_chain():
    program = JQCompiler().parse(".people[] | select(.active)")
    expression = program.expression
    assert isinstance(expression, BinaryExpression)
    assert expression.operator == "|"
    assert isinstance(expression.left, IndexExpression)
    assert isinstance(expression.right, CallExpression)


def test_parser_builds_object_and_literals():
    program = JQCompiler().parse('{name: .user, admin: true, score: 1.2e3}')
    expression = program.expression
    assert isinstance(expression, ObjectExpression)
    assert [field.key for field in expression.fields] == ["name", "admin", "score"]
    assert expression.fields[1].value == Literal(span=expression.fields[1].value.span, value=True)
    assert expression.fields[2].value.value == Decimal("1.2e3")


def test_parser_builds_conditionals():
    program = JQCompiler().parse('if .age >= 18 then "adult" else "child" end')
    expression = program.expression
    assert isinstance(expression, ConditionalExpression)
    assert len(expression.branches) == 1
    assert expression.fallback.value == "child"
