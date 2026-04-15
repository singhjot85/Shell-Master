"""Configurable formatting rules for the jq pretty-printer."""

from __future__ import annotations

from dataclasses import dataclass


DEFAULT_INDENT_UNIT = "    "
DEFAULT_NEWLINE = "\n"
DEFAULT_PIPE_OPERATOR = "|"
DEFAULT_COMMA_OPERATOR = ","
DEFAULT_SPACE = " "
DEFAULT_FUNCTION_ARGUMENT_SEPARATOR = ";"
DEFAULT_EMPTY_ARRAY = "[]"
DEFAULT_EMPTY_OBJECT = "{}"

DEFAULT_COMPACT_CALL_MAX_ARGS = 3
DEFAULT_COMPACT_ARRAY_MAX_ITEMS = 3
DEFAULT_COMPACT_OBJECT_MAX_FIELDS = 2


@dataclass(slots=True)
class FormatterRules:
    """Formatting knobs that control how jq is rendered.

    Keep all user-tweakable pretty-printing policy here so changes stay local.
    """

    indent_unit: str = DEFAULT_INDENT_UNIT
    newline: str = DEFAULT_NEWLINE
    pipe_operator: str = DEFAULT_PIPE_OPERATOR
    comma_operator: str = DEFAULT_COMMA_OPERATOR
    space: str = DEFAULT_SPACE
    function_argument_separator: str = DEFAULT_FUNCTION_ARGUMENT_SEPARATOR
    empty_array: str = DEFAULT_EMPTY_ARRAY
    empty_object: str = DEFAULT_EMPTY_OBJECT
    compact_call_max_args: int = DEFAULT_COMPACT_CALL_MAX_ARGS
    compact_array_max_items: int = DEFAULT_COMPACT_ARRAY_MAX_ITEMS
    compact_object_max_fields: int = DEFAULT_COMPACT_OBJECT_MAX_FIELDS
    multiline_calls: bool = True
    multiline_arrays: bool = True
    multiline_objects: bool = True
    multiline_pipelines: bool = True
    multiline_conditionals: bool = True
