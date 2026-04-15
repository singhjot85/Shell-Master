# Architecture

`jqtools` is organized as a layered project:

1. Core compiler: `src/jqtools/compiler`
2. Tooling layer: `src/jqtools/tooling`
3. Interface layer: `src/jqtools/cli.py`

## Core compiler

The core owns:

- A position-aware source reader
- A token model and lexer
- A top-down Pratt parser
- A typed AST and compiler facade

## Tooling layer

The second layer consumes compiler output instead of reparsing strings:

- `JQFormatter` renders the AST back into readable jq
- `JQDebugger` exposes structured debug reports, trace frames, and runtime-adapter hooks

## Interface layer

The CLI is thin by design so future interfaces can reuse the same compiler and
tooling APIs:

- direct Python API calls
- VS Code extension entrypoints
- automation runners or service adapters

## Current jq coverage

The foundation currently supports:

- literals: strings, numbers, booleans, `null`
- accessors and variables: `.`, `.name`, `$var`
- arrays and objects
- function calls
- indexing: `[expr]`, `[]`, and optional `?`
- infix operators: `|`, `,`, `+`, `-`, `*`, `/`, `%`, comparisons, `and`, `or`, `//`
- conditionals: `if / then / elif / else / end`
