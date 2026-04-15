"""Examples for embedding jqtools in Python code."""

from jqtools import JQCompiler, JQDebugger, JQFormatter


compiler = JQCompiler()
result = compiler.compile('.people[] | {name: .name, active: true}')

print("TOKENS")
for token in result.tokens:
    print("\t", token)

print("\nFORMATTED")
print("\t", JQFormatter().render_program(result.ast))

print("\nTRACE")
for line in JQDebugger().trace(".people[] | .name").ast_summary:
    print("\t", line)
