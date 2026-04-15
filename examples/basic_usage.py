"""Examples for embedding jqtools in Python code."""

from jqtools import JQCompiler, JQDebugger, JQFormatter

with open("examples\example.jq", "r") as f:
    jq_program = f.read()

compiler = JQCompiler()
result = compiler.compile(jq_program)

formatted = JQFormatter().render_program(result.ast)
with open("examples\\formatted.jq", "w") as f:
    f.write(formatted)