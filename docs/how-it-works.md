# How It Works

`jqtools` is built in three layers so each concern stays small and reusable.

## Flow

1. Source goes into the compiler.
2. The lexer turns text into tokens.
3. The Pratt parser turns tokens into an AST.
4. Tooling reads that AST to format or debug jq.
5. The CLI or other integrations call those APIs.

## Main Parts

### `src/jqtools/compiler`

This is the engine room.

- `errors.py`
  Defines compiler-specific errors and source locations.
- `inputs.py`
  Tracks characters, offsets, lines, and columns while reading source.
- `tokens.py`
  Defines token kinds, keyword mapping, and the token model.
- `lexer.py`
  Scans jq source into tokens.
- `ast.py`
  Defines AST nodes like literals, accessors, objects, arrays, and binary expressions.
- `parser.py`
  Implements the top-down Pratt parser and operator precedence.
- `compiler.py`
  Provides `JQCompiler`, the high-level facade for `tokenize`, `parse`, and `compile`.

### `src/jqtools/tooling`

This is the second layer built on top of compiler output.

- `formatter.py`
  Re-renders supported AST nodes into readable jq.
- `debugger.py`
  Produces token and AST traces for inspection.

### `src/jqtools`

This is the public package surface.

- `__init__.py`
  Re-exports the main compiler and tooling APIs.
- `cli.py`
  Defines CLI commands like `tokenize`, `parse`, `format`, and `debug`.
- `__main__.py`
  Supports `python -m jqtools`.

## Other Folders

- `automations/`
  Compatibility shims for the older package path.
- `tests/`
  Unit and smoke-style tests for compiler and tooling behavior.
- `examples/`
  Small runnable examples for local exploration.
- `docs/`
  Project documentation and architecture notes.

## File Interaction

- `lexer.py` depends on `inputs.py`, `tokens.py`, and `errors.py`
- `parser.py` depends on `tokens.py`, `ast.py`, and `errors.py`
- `compiler.py` ties `lexer.py` and `parser.py` together
- `formatter.py` and `debugger.py` depend on the compiler layer
- `cli.py` depends on compiler and tooling, but keeps no parsing logic itself

## Typical Use

### Tokenize

```bash
poetry run jqtools tokenize ".name | .age"
```

### Parse

```bash
poetry run jqtools parse ".people[] | select(.active)"
```

### Format

```bash
poetry run jqtools format "{name:.user,items:[1,2,3]}"
```

### Debug

```bash
poetry run jqtools debug ".name | length"
```

## Mental Model

- Compiler layer: understands jq structure
- Tooling layer: uses that structure
- Interface layer: exposes it to users and future integrations
