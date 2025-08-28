from . import Token, TokenType, LexerError
from .constants import STRING_MAPPING, KEYWORDS_MAPPING, BRACKET_MAPPING

class Lexer:
    """ Implements the algorithm for lexical analyzer """
    def __init__(self, source: str):
        """ keeping the logic of lines and columns as we need it in debugger """
        self.program = source
        self.current = 0
        self.line = 0
        self.col = 0

        self.program_size = len(self.program)

        # Token Tracking
        self._token_start_idx = 0
        self._token_line = 0
        self._token_col = 0

    def tokenize(self) -> list[TokenType] | None:
        """ Return a list of valid JQ tokens given a string of JQ program"""
        tokens :list[Token] = []

        while self.current <= self.program_size:
            ch: str = self._advance()
            
            if ch in [' ', '\t', '\r']: # Skip whitespaces
                continue
            if ch == '\n': # Reset line no. on a newline
                self.col = 0
                self.line += 1
                continue
            if ch == '#': # Skip comments as of now
                # TODO: handle Comments
                self.skip_comments()
                continue

            if ch == '"': # Handle Strings
                tokens.append(self.scan_string())
                continue

            if ch.isdigit() or (ch=='-' and self._peek().isdigit()):
                # Handles Integers/Floats
                tokens.append(self.scan_number(ch))
                continue

            if ch == '$': # Handle Variables
                tokens.append(self.scan_variable)
                continue
                
            if self._is_ident_begin(ch): # Handle Identifiers and Keywords
                tokens.append(self.scan_identifier_or_keywords(ch))
            
            if token := self.scan_operator_or_punct(ch):
                tokens.append(token)
                continue
    
    ###### Helpers ######

    def _advance(self) -> str:
        """ To advance in traversal """
        if self.current + 1 <= self.program_size:
            char = self.program[self.current]
            self.current += 1
            self.col += 1
            return char
        else:
            # raise LexerError(msg="Error in iteration", line=self.line, col=self.col)
            return None
    
    def _peek(self) -> str:
        """ Peek one element ahead """
        if self.current + 1 <= self.program_size:
            return self.program[self.current + 1]
        else:
            # raise LexerError(msg="Error in peek", line=self.line, col=self.col)
            return None
    
    def _peek_peek(self) -> str:
        """ Peek two elements ahead """
        if self.current + 2 <= self.program_size:
            return self.program[self.current + 2]
        else:
            # raise LexerError(msg="Error in peek peek", line=self.line, col=self.col)
            return None

    def _mark_token_start(self):
        """ Mark the start of a token, with  """
        self._token_start_idx = self.current
        self._token_line = self.line
        self._token_col = self.col
    
    def _create_token(self, ttype: TokenType, value=None) -> Token:
        """ Create a token given a token_type and value """
        return Token(ttype, value, self._token_line, self._token_col)
    
    ###### Handles ######

    def skip_comments(self) -> None:
        """ Skips line with comments """
        while (
            self.current <= self.program_size 
            and self.program[self.current] != '\n'
        ):
            self.current += 1
        self.line += 1
        self.col = 0

    def scan_string(self) -> str:
        """ Scans for a string and returns a string Token """
        ret: list = []
        while self.current <= self.program_size:
            c = self._advance()
            if c == '"': # End of String
                return self._create_token(TokenType.STRING, ''.join(ret))
            
            if c == "\\":
                esc = self._advance()
                if esc in '"\\/bfnrt':
                    ret.append(STRING_MAPPING[esc])
                elif esc == "u": # Read exactly 4 hex digits
                    hex_digits = [self._advance() for _ in range(4)]
                    if not all(d.lower() in '0123456789abcdef' for d in hex_digits): 
                        LexerError(
                            msg="Invalid \\u escape",
                            line=self.line,col=self.col
                        )
                    codepoint = int(''.join(hex_digits), 16)
                    ret.append(chr(codepoint))
            elif c == '\n': # Newline inside stings
                raise LexerError(
                    msg="Unterminated String (Newline)",
                    line=self.line,col=self.col
                )
            else:
                ret.append(c)
            
        return LexerError(
            msg="Unterminated String (EOF)",
            line=self.line,col=self.col
        )
    
    def scan_number(self, first: str) -> Token:
        buf = [first]

        # Integer's
        while self._peek().isdigit():
            buf.append(self._advance())

        # Fractions
        if self._peek() == '.' and self._peek_peek().isdigit():
            buf.append(self._advance())
            while self._peek().isdigit():
                buf.append(self._advance())

        # Exponent
        if self._peek() in 'eE':
            buf.append(self._advance())  # e/E
            if self._peek() in '+-':
                buf.append(self._advance())
            if not self._peek().isdigit():
                raise LexerError(
                    msg="Malformed exponent",
                    line=self.line,col=self.col
                )
            while self._peek().isdigit():
                buf.append(self._advance())
        
        text = ''.join(buf)
        
        # choose int vs float
        value = None
        try:
            if any(ch in text for ch in '.eE'):
                value = float(text)
            else:
                value = int(text)
        except ValueError:
            raise LexerError(
                msg="Invalid number",
                line=self.line,col=self.col
            )

        return self._create_token(TokenType.NUMBER, value)

    def _is_ident_begin(self, ch:str) -> bool:
        return ch.isalpha() or ch == '_'
    
    def _is_ident(self, ch:str) -> bool:
        return ch.isalnum or ch == '_'
    
    def scan_variable(self) -> TokenType:

        if not self._is_ident_begin(self._peek()):
            raise LexerError(
                msg=f"Invalid variable name start - [{self._peek()}]", 
                line=self.line, col=self.col
            )
        
        buf = []
        while self._is_ident(self._peek()):
            buf.append(self._advance())
        
        name = ''.join(buf)
        return self._create_token(TokenType.VARIABLE, name)
    
    def scan_identifier_or_keywords(self, first: str) -> Token:
        buf = [first]

        while self._is_ident(self._peek()):
            buf.append(self._advance())
        
        text = ''.join(buf)

        ttype = KEYWORDS_MAPPING.get(text)
        if ttype is None:
            return self._create_token(TokenType.IDENTIFIER, text)
        else:
            # TODO: Attach semantic value for literals
            if ttype is TokenType.NULL:
                return self._create_token(TokenType.NULL, None)
            if ttype is TokenType.TRUE:
                return self._create_token(TokenType.TRUE, True)
            if ttype is TokenType.FALSE:
                return self._create_token(TokenType.FALSE, False)
            
            return self._create_token(ttype, text)
    
    def _match(self, expected: str) -> bool:
        if (
            self.current <= self.program_size 
            or self.program[self.current] != expected
        ):
            return False
        self.current += 1
        self.col += 1
        return True

    def scan_operator_or_punct(self, c:str) -> Token | None:
        if c == '/':
            if self._match('/'):
                return self._create_token(TokenType.ALT, '//')
            return self._create_token(TokenType.SLASH, '/')
        if c == '=' and self._match('='):
            return self._create_token(TokenType.EQ, '==')
        if c == '!' and self._match('='):
            return self._create_token(TokenType.NEQ, '!=')
        if c == '<':
            if self._match('='):
                return self._create_token(TokenType.LTE, '<=')
            return self._create_token(TokenType.LT, '<')
        if c == '>':
            if self._match('='):
                return self._create_token(TokenType.GTE, '>=')
            return self._create_token(TokenType.GT, '>')

    def scan_for_brackets(self, ch: str) -> Token | None:
        brackets = [
            TokenType.LPAREN, TokenType.RPAREN, TokenType.LSQRBRC, 
            TokenType.RSQRBRC, TokenType.LCURLBRC, TokenType.RCURLBRC
        ]
        if (
            self.current <= self.program_size 
            and ch in brackets
        ):
            return self._create_token(BRACKET_MAPPING[ch])
        return None