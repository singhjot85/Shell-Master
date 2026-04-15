# jqtools

`jqtools` is a compiler-first project for building jq automation tooling.

## Layers

- Core compiler: position-aware lexer plus a top-down Pratt parser
- Tooling layer: formatter and structural debugger built on compiler output
- Interface layer: a CLI today, with room for APIs, editors, and automation integrations

## Project layout

```text
src/jqtools/
  compiler/
  tooling/
  cli.py
automations/
docs/
examples/
tests/
```

## Quick start

```bash
poetry install
poetry run jqtools tokenize ".name | {greeting: \"hi\"}"
poetry run jqtools parse ".people[] | select(.active)"
poetry run jqtools format "{name:.user,items:[1,2,3]}"
poetry run jqtools debug "if .age >= 18 then \"adult\" else \"child\" end"
```

## Python usage

```python
from jqtools import JQCompiler, JQDebugger, JQFormatter

compiler = JQCompiler()
result = compiler.compile(".people[] | {name: .name}")

print(result.tokens)
print(JQFormatter().render_program(result.ast))
print(JQDebugger().trace(".people[] | .name").ast_summary)
```

## Documentation

- [Architecture](docs/architecture.md)
- [How It Works](docs/how-it-works.md)
- [Formatter Internals](docs/formatter-how-it-works.md)
- [Tweaking Pretty-Printing](docs/tweaking-pretty-printing.md)
- [Example usage](examples/basic_usage.py)
