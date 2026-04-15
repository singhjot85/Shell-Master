"""Tests for formatter and debugger layers."""

from jqtools import JQDebugger, JQFormatter


def test_formatter_renders_supported_subset():
    rendered = JQFormatter().format('{name:.user,items:[1,2,3]}')
    assert rendered == "{name: .user, items: [1, 2, 3]}"


def test_debugger_emits_trace():
    trace = JQDebugger().trace(".name | length")
    assert any("PIPE" in item for item in trace.token_summary)
    assert any("Program" in item for item in trace.ast_summary)
