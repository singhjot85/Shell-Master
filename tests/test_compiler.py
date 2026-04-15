"""High-level tests for the jq compiler core."""

from decimal import Decimal

from jqtools.compiler import (
    AsExpression,
    BinaryExpression,
    CallExpression,
    ConditionalExpression,
    FunctionDefinition,
    IndexExpression,
    JQCompiler,
    Literal,
    ObjectExpression,
    ReduceExpression,
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


def test_parser_builds_top_level_function_definitions():
    program = JQCompiler().parse('def add(a; b): a + b; add(1; 2)')
    assert len(program.definitions) == 1
    definition = program.definitions[0]
    assert isinstance(definition, FunctionDefinition)
    assert definition.name == "add"
    assert definition.parameters == ["a", "b"]
    assert isinstance(definition.body, BinaryExpression)
    assert isinstance(program.expression, CallExpression)


def test_parser_supports_multiple_definitions_before_main_expression():
    program = JQCompiler().parse('def inc(x): x + 1; def double(x): x * 2; .value | inc | double')
    assert [definition.name for definition in program.definitions] == ["inc", "double"]
    assert isinstance(program.expression, BinaryExpression)


def test_parser_builds_as_binding_expression():
    program = JQCompiler().parse('.[] as $item | . + $item')
    assert isinstance(program.expression, AsExpression)
    assert program.expression.variable == "$item"
    assert isinstance(program.expression.body, BinaryExpression)


def test_parser_builds_reduce_expression():
    program = JQCompiler().parse('reduce .[] as $i (0; . + $i)')
    assert isinstance(program.expression, ReduceExpression)
    assert program.expression.variable == "$i"
    assert isinstance(program.expression.update, BinaryExpression)
