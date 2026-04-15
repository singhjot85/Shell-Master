# Tweaking Pretty-Printing Rules

All formatting policy lives in `src/jqtools/tooling/formatter_rules.py`.

Use `FormatterRules` to tweak output without rewriting the formatter engine.

## Main Rule Knobs

- `indent_unit`
  Controls one indentation level
- `newline`
  Controls line breaks
- `compact_call_max_args`
  Max call arguments allowed before multiline formatting
- `compact_array_max_items`
  Max array items allowed before multiline formatting
- `compact_object_max_fields`
  Max object fields allowed before multiline formatting
- `multiline_calls`
  Turn multiline call formatting on or off
- `multiline_arrays`
  Turn multiline array formatting on or off
- `multiline_objects`
  Turn multiline object formatting on or off
- `multiline_pipelines`
  Turn multiline pipeline formatting on or off
- `multiline_conditionals`
  Turn multiline conditional formatting on or off

## Example

```python
from jqtools import JQFormatter
from jqtools.tooling import FormatterRules

rules = FormatterRules(
    indent_unit="  ",
    compact_array_max_items=2,
    compact_object_max_fields=1,
)

formatter = JQFormatter(rules=rules)
print(formatter.format('{name:.user,items:[1,2,3]}'))
```

## Recommended Workflow

1. Change only `FormatterRules` first when possible.
2. If a new layout style is needed, update the matching `_build_*_doc()` method.
3. Add or update formatter tests after every rule change.
4. Keep literal output tokens and spacing constants centralized.

## When To Change Rules Vs Logic

Change rules when:

- indentation size changes
- compact thresholds change
- a multiline style is enabled or disabled

Change formatter logic when:

- a new AST node needs formatting
- a new layout strategy is introduced
- line break placement rules become structurally different

## Goal

The goal is to make pretty-printing policy easy to tune while keeping the
formatter engine stable.
