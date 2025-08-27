class LexerError(Exception):
    pass

def lexer_error_msg(msg:str, line: int, col: int) -> str:
    return f"Error occurred while lexing at [{line}:{col}]: {msg}"
