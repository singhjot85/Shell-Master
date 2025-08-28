class LexerError(Exception):
    """ Error class for Lexer """
    def __init__(self, **kwargs):
        self.line = kwargs.get("line", 0)
        self.column = kwargs.get("col", 0)
        self.message = kwargs.get("msg", "Unkown error")
        super().__init__(f"Error occurred while lexing at [{self.line}:{self.column}]: {self.message}")