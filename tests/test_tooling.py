"""Tests for formatter and debugger layers."""

from jqtools import FormatterRules, JQDebugger, JQFormatter


def test_formatter_renders_supported_subset():
    rendered = JQFormatter().format('{name:.user,items:[1,2,3]}')
    assert rendered == "{\n    name: .user,\n    items: [1, 2, 3]\n}"


def test_formatter_breaks_large_pipeline_into_lines():
    rendered = JQFormatter().format(
        '.people[] | select(.active == true) | {name: .name, emails: [.email, "unknown"]}'
    )
    assert rendered == (
        ".people[]\n"
        "| select(\n"
        "    .active == true\n"
        ")\n"
        "| {\n"
        "    name: .name,\n"
        '    emails: [.email, "unknown"]\n'
        "}"
    )


def test_formatter_renders_multiline_conditionals():
    rendered = JQFormatter().format('if .age >= 18 then "adult" else "child" end')
    assert rendered == 'if .age >= 18 then\n    "adult"\nelse\n    "child"\nend'


def test_formatter_renders_program_definitions_before_main_expression():
    rendered = JQFormatter().format('def add(a; b): a + b; def double(x): x * 2; .value | add(1; 2) | double')
    assert rendered == (
        "def add(a; b):\n"
        "    a + b;\n"
        "\n"
        "def double(x):\n"
        "    x * 2;\n"
        "\n"
        ".value\n"
        "| add(1; 2)\n"
        "| double"
    )


def test_formatter_renders_as_binding_and_reduce():
    formatter = JQFormatter()
    binding = formatter.format('.[] as $item | . + $item')
    reduce_expr = formatter.format('reduce .[] as $i (0; . + $i)')
    assert binding == ".[] as $item\n| . + $item"
    assert reduce_expr == "reduce .[] as $i (\n    0;\n    . + $i\n)"


def test_formatter_rules_allow_custom_indent_and_compactness():
    formatter = JQFormatter(
        rules=FormatterRules(
            indent_unit="  ",
            compact_array_max_items=2,
            compact_object_max_fields=1,
        )
    )
    rendered = formatter.format('{name:.user,items:[1,2,3]}')
    assert rendered == "{\n  name: .user,\n  items: [\n    1,\n    2,\n    3\n  ]\n}"


def test_debugger_emits_trace():
    trace = JQDebugger().trace(".name | length")
    assert any("PIPE" in item for item in trace.token_summary)
    assert any("Program" in item for item in trace.ast_summary)
