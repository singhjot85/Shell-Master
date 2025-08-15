import re
from . import BaseParser

class JQFormatter:
    def __init__(self, jq_program):
        parser = BaseParser(jq_program)
        self.program = ''
        if isinstance(jq_program, str):
            self.program = parser.parse_sts()

"Minor change"





STRING_PATTERN = r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\''
COMMENT_PATTERN = r'#.*?$'
TOKEN_PATTERN = rf'{STRING_PATTERN}|[\[\]\{{\}}\(\)\|,]|[^\[\]\{{\}}\(\)\|,#\s]+|{COMMENT_PATTERN}'

def format_jq(program: str, indent_width: int = 4) -> str:
    """
    Formats a JQ program into a readable, consistent style.
    Preserves comments and quoted strings.
    """
    tokens = re.findall(TOKEN_PATTERN, program, re.MULTILINE)
    indent = 1
    formatted_lines = []
    current_line = []

    def flush_line():
        if current_line:
            formatted_lines.append(" " * (indent * indent_width) + " ".join(current_line).rstrip())
            current_line.clear()

    for token in tokens:
        token = token.strip("\n\r ")
        if not token:
            continue

        # Comments: put them on their own line
        if token.startswith("#"):
            flush_line()
            formatted_lines.append(" " * (indent * indent_width) + token)
            continue

        # Closing brackets
        if token in ["]", "}", ")"]:
            flush_line()
            indent -= 1

        current_line.append(token)

        # After opening brackets
        if token in ["[", "{", "("]:
            flush_line()
            indent += 1
        # After commas and pipes
        elif token in [",", "|"]:
            flush_line()

        # Closing brackets again flush immediately
        if token in ["]", "}", ")"]:
            flush_line()

    flush_line()
    return "\n".join(formatted_lines)


