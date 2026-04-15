# Debugger Design

The debugger is designed as a tooling-layer service with a runtime adapter seam.

## Goals

- pinpoint the jq failure line and expression
- expose the input context available at that point
- distinguish direct failures from cascading failures
- support two modes:
  - `failure_only`
  - `detailed`
- keep output structured so a VS Code extension can reuse it with minimal glue

## Modes

### `failure_only`

Use this for faster runs.

The debugger returns:

- failure message
- failure line and column
- jq expression/snippet at the failure point
- execution trace leading to the failure

### `detailed`

Use this when full runtime insight matters.

The debugger can additionally include:

- input JSON visible at each frame
- variable bindings visible at each frame
- failure-time input context

This mode is intentionally optional because capturing every snapshot can become
 expensive on large jq programs or large inputs.

## Architecture

### Compiler layer

The compiler already provides:

- tokens
- AST nodes with source spans
- parse errors with source location

### Tooling layer

The debugger adds:

- `DebugMode`
- `DebugReport`
- `ExecutionFrame`
- `DebugFailure`
- `RuntimeContextSnapshot`

These are serializable-friendly models intended for APIs, UIs, and editor
 integrations.

### Runtime adapter seam

The debugger is split into:

- source/AST aware tooling
- a runtime adapter interface

Files:

- `src/jqtools/tooling/debugger.py`
- `src/jqtools/tooling/debugger_models.py`
- `src/jqtools/tooling/debugger_runtime.py`
- `src/jqtools/tooling/debugger_source.py`

The runtime adapter can later be backed by:

- a Python evaluator
- a jq subprocess wrapper
- a remote debugging service

## VS Code Extension Fit

This design is editor-friendly because the extension would only need to:

1. send jq source and input JSON
2. choose `failure_only` or `detailed`
3. render `DebugReport`

The extension does not need to understand parser internals or AST traversal.

## Current Status

Right now the debugger supports:

- compile/parser failure reporting
- source-span based expression snippets
- static trace frames
- a stable runtime adapter seam for future execution tracing

The next step is plugging in a real runtime backend that emits trace events and
failure events tied to AST node ids.
