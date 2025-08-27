This will be the core for jq parsing, the approach here is to develop a parse,
the parder will parse the jq-program to an AST(Abstract Syntax Tree), this will be done in two steps:
1. Tokenize the given input into keywords, identifiers, literals etc.
2. Parse the tokens to AST.

```
jq_core/
│
├── __init__.py      # makes this a package
├── main.py          # entry point for running jq_core from CLI
│
├── lexer.py         # Phase 1: tokenization logic
├── tokens.py        # Token type definitions
├── ast.py           # AST node definitions
├── parser.py        # Phase 2: parser implementation
├── errors.py        # Custom error classes (LexerError, ParserError, etc.)
│
└── tests/           # tests for each phase
    ├── __init__.py
    ├── test_lexer.py
    ├── test_parser.py
    └── ...
```


## Phase 1 – Tokenizer (Lexer)
1. Define token types (keywords, identifiers, literals, operators, punctuation).
    - a token is the atomic unit (word/symbol) from source code.
    - directly parse from raw text but its error-prone and messy.
2. Implement a scanner:
    - Single-pass, reading character by character.
    - Recognize literals (123, "string"), identifiers, keywords, comments.
    - Track line/column for errors.
    - Skip whitespace & comments.
3. Build unit tests:
    -  Input to list of tokens (with type and value).
    Example:
    ```
    Input: .foo | 42
    Output: IDENTITY, DOT_FIELD("foo"), PIPE, NUMBER(42)
    ```

## Phase 2 – AST Node Definitions
1. Define AST classes (Python dataclass).
    - AST (Abstract Syntax Tree) = structured representation of program’s meaning.
    - can also build concrete syntax tree (keeps every detail like parentheses, whitespace) that's heavier, less portable.
2. Keep nodes simple (just data, no logic).
3. Plan for serialization (JSON export).

## Phase 3 – Parser (Pratt parser for expressions)

1. Implement a Pratt parser (top-down operator precedence).
    - Why Pratt? jq is expression-heavy with lots of infix/postfix operators; Pratt is flexible.
    - Alternatives: 
        - Recursive descent (works, but precedence handling is painful).
        - Parser generators (ANTLR, Lark, Bison) are more automatic, less learning by hand.
    - Pratt is used: JavaScript parsers, expression evaluators in many DSLs.

2. Define binding power table (operator precedence).
3. Implement nud (null denotation → literals, prefix ops) and led (left denotation → infix/postfix ops).
Parse examples:
```
.foo | .bar
1 + 2 * 3
if . > 5 then "big" else "small" end
```

## Phase 4 – Driver + Debugging

- A main.py that:
    - Reads jq snippet from stdin.
    - Runs lexer -> prints tokens.
    - Runs parser -> prints AST.