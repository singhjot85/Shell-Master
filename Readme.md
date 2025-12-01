Design:

- Use an abstract InputSource (string, bytes, byte-stream).
    - String Input
    - Bytes Input
    - Byte-Stream Input (for scale)
- Design a position-aware lexer
    - Token type
    - Start + end positions (line, column)
    - Raw lexeme
    - Token category (operator, identifier, literal, pipe, filter, etc.)
- Implement recursive descent parser with jq’s precedence model
- Build AST nodes with complete source-span metadata
    - Preserve comments + whitespace in a “trivia” structure

1. Debugger
    - Instrumentation around AST eval
    - Structured error handling
2. Formatter
    - AST visitor → pretty-printer, not regex or string hacks

This design can easily scale into:
- LSP server (syntax highlighting + jump to definition)
- auto-completion tools
- jq refactoring tools


To-do list:
- [ ] jq grammar (complete formal grammar)
- [ ] AST class definitions (Python, TS, Go)
- [ ] Lexer implementation blueprint
- [ ] Error-handling architecture (panic mode, LL recovery)
- [ ] Prototype of a jq debugger (pseudo-code)
- [ ] Formatter visitor template

Progress Tracker:
- [X] Handlers
    - [ ] Tests
- [x] Lexer
    - [X] Proper tokentype/ category
    - [X] Proper raw lexeme data
    - [X] Proper lexeme position
    - [x] Tests
- [ ] Parser
    - [ ] Grammar
    - [ ] Proper AST nodes
    - [ ] AST Structure
    - [ ] Tests
- [ ] Debugger
- [ ] Formatter
- [ ] Auto-complete
