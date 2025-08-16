import re
from . import BaseParser

import re
import json

class JQFormatter:
    def __init__(self, indent_size: int = 4):
        self.program = ''
        self.parser = BaseParser()
        self.indent_size = 4

    def extract_tokens(self, input_str: str):
        pass

    def extract_base_jq(self, jq_program: str):
        pass
    
    def format(self, jq_program):

        if isinstance(jq_program, str):
            self.program = self.parser.parse_sts(jq_program)
        else:
            self.program = ''

        pre, root, post = self.extract_base_jq(self.program)
        tokens = self.tokenize_jq(root)
        for key, jq in tokens.items():
            # TODO: Figure out base/root condition.
            # if root:
            #     continue
            tokens[key] = self.format(jq)
            



    def tokenize_jq(program: str):

        def parse_object(obj_str: str):
            tokens = {}
            is_string = False
            key = None
            start = 1  # skip leading '{'

            brace_depth = 0
            bracket_depth = 0

            i = 1
            while i < len(obj_str)-1:  # skip trailing '}'
                ch = obj_str[i]

                # Toggle string state (ignore escaped quotes)
                if ch == '"' and obj_str[i-1] != '\\':
                    is_string = not is_string

                elif not is_string:
                    if ch == '{':
                        brace_depth += 1
                    elif ch == '}':
                        brace_depth -= 1
                    elif ch == '[':
                        bracket_depth += 1
                    elif ch == ']':
                        bracket_depth -= 1

                    elif ch == ':' and brace_depth == 0 and bracket_depth == 0 and key is None:
                        key = obj_str[start:i].strip()
                        start = i+1

                    elif ch == ',' and brace_depth == 0 and bracket_depth == 0 and key is not None:
                        value = obj_str[start:i].strip()
                        tokens[key] = parse_value(value)
                        key = None
                        start = i+1

                i += 1

            # Handle last key:value before '}'
            if key is not None and start < len(obj_str)-1:
                value = obj_str[start:len(obj_str)-1].strip()
                tokens[key] = parse_value(value)

            return tokens

        def parse_array(arr_str: str):
            items = []
            is_string = False
            start = 1  # skip '['

            brace_depth = 0
            bracket_depth = 0

            i = 1
            while i < len(arr_str)-1:  # skip ']'
                ch = arr_str[i]

                if ch == '"' and arr_str[i-1] != '\\':
                    is_string = not is_string

                elif not is_string:
                    if ch == '{':
                        brace_depth += 1
                    elif ch == '}':
                        brace_depth -= 1
                    elif ch == '[':
                        bracket_depth += 1
                    elif ch == ']':
                        bracket_depth -= 1

                    elif ch == ',' and brace_depth == 0 and bracket_depth == 0:
                        items.append(parse_value(arr_str[start:i].strip()))
                        start = i+1

                i += 1

            # Last item
            if start < len(arr_str)-1:
                items.append(parse_value(arr_str[start:len(arr_str)-1].strip()))

            return items

        def parse_value(val: str):
            if val.startswith("{") and val.endswith("}"):
                return parse_object(val)
            elif val.startswith("[") and val.endswith("]"):
                return parse_array(val)
            else:
                return val  # primitive (number, string, bool, null, jq expr)

        return parse_value(program)
