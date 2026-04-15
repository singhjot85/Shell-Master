# Formatter How It Works

The jq formatter is split into two concerns:

1. Formatting mechanics
2. Formatting policy

## Mechanics

The mechanics live in `src/jqtools/tooling/formatter.py`.

The formatter does not build the output by directly concatenating lots of jq
strings. Instead, it builds a small document tree:

- `Text`
  Raw output text
- `Line`
  A newline plus an indentation depth change
- `Concat`
  A list of document nodes rendered in order

This makes indentation predictable for large jq files because indentation is
tracked as depth, not guessed from previous strings.

## Flow

1. `JQFormatter.format()` parses source into an AST.
2. `_build_expression_doc()` converts AST nodes into document nodes.
3. `_render_doc()` walks the document tree.
4. `_emit()` writes the final formatted string using the current depth.

## Why this scales

- Pipelines can be flattened and rendered stage by stage.
- Arrays and objects can decide between compact and multiline layout.
- Indentation is controlled centrally by `Line(indent_delta=...)`.
- The formatter returns one final string, so consumers can render it directly.

## File Roles

- `src/jqtools/tooling/formatter.py`
  Pretty-print engine and doc tree renderer
- `src/jqtools/tooling/formatter_rules.py`
  Rule definitions and tweakable constants
- `src/jqtools/compiler/parser.py`
  Produces the AST that the formatter consumes

## Important Design Choice

Formatting decisions should come from rules, not scattered magic strings.

For example:

- indent unit is defined once
- newline is defined once
- compact thresholds are defined once
- multiline toggles are defined once

That keeps experiments low-risk and easy to review.
