from decimal import Decimal
from . import Token, TokenType, LexerError
from .constants import (
    STRING_MAPPING, 
    KEYWORDS_MAPPING, 
    WHITE_SPACES,
    NEW_LINES,
    COMMENT_HASH,
    STRING_QUOTE,
    BRACKETS
)

class Lexer:
    """ Implements the algorithm for lexical analyzer """

    def __init__(self, source: str):
        """ keeping the logic of lines and columns as we need it in debugger """
        
        self.program: str = source
        self.program_size: int = len(self.program)
        
        self.current: str = self.program[0] if self.program else None
        self.current_idx: int = 0
        self.line: int = 0
        self.col: int = 0

        print(f"Lexical Analyzer initialized program_size:{self.program_size}")

    def tokenize(self) -> list[TokenType] | None:
        """ Return a list of valid JQ tokens given a string of JQ program"""
        tokens :list[Token] = []

        while not self._is_end():
            ch = self.current
            if not ch:
                break

            # Not required (Can be made flag enabled if required in future).
            # if ch in WHITE_SPACES:
            #     continue
            if ch in NEW_LINES:
                self._line_break()
            if ch == COMMENT_HASH: # Skip comments as of now
                # TODO: handle Comments
                self.skip_comments()
                continue

            if ch in BRACKETS:
                tokens.append(self._create_token(BRACKETS[ch]))
            if ch == TokenType.COMMA.value:
                tokens.append(self._create_token(TokenType.COMMA))
            if ch == TokenType.COLON.value:
                tokens.append(self._create_token(TokenType.COLON))
            if ch == TokenType.PIPE.value:
                tokens.append(self._create_token(TokenType.PIPE))
            
            if ch == TokenType.DOT.value:
                tokens.extend(self.handle_accessor())
                continue
            if self._is_identifier_begin(ch):
                tokens.append(self.handle_identifier())
                continue
            if ch == STRING_QUOTE: # Handle Strings
                tokens.append(self.scan_string())
                continue
            if ch.isdigit() or (ch=='-' and self._peek().isdigit()):
                # Handles Integers/Floats/Exponents
                tokens.append(self.scan_number())
                continue

            # if ch == '$': # Handle Variables
            #     tokens.append(self.scan_variable())
            #     continue
                
            # if self._is_identifier_begin(ch): # Handle Identifiers and Keywords
            #     tokens.append(self.scan_identifier_or_keywords(ch))
            
            # if token := self.scan_operator_or_punct(ch):
            #     tokens.append(token)
            #     continue

            self._advance()

        print(f"Total Tokens: {tokens}")
        return tokens
    
    ###### Helpers ######

    def _is_end(self) -> bool:
        return not (self.current_idx < self.program_size)

    def _line_break(self) -> None:
        self.col = 0 
        self.line += 1
    
    def _is_identifier_begin(self, ch:str) -> bool:
        if not ch:
            return False
        return ch.isalpha() or ch == '_'
    
    def _is_identifier(self, ch:str) -> bool:
        if not ch:
            return False
        return ch.isalnum() or ch == '_'

    def _advance(self) -> str:
        """ moves to next character and returns it """
        if self.current_idx < self.program_size:
            self.current_idx += 1
            self.col += 1
            if self._is_end():
                self.current = None
                return None
            else:
                self.current = self.program[self.current_idx]
                return self.current
        else:
            self.current = None
            return None
    
    def _peek(self) -> str:
        """ returns the next character does not move the pointer """
        if self.current_idx + 1 < self.program_size:
            return self.program[self.current_idx + 1]
        else:
            return None
    
    def _peek_peek(self) -> str:
        """ returns next to next character does not move the pointer """
        if self.current_idx + 2 < self.program_size:
            return self.program[self.current_idx + 2]
        else:
            return None
    
    def _create_token(self, ttype: TokenType, value=None) -> Token:
        """ Create a token given a token_type and value """
        token = None
        if not value:
            token = Token(ttype, ttype.value, 0, 0)
        else:
            token = Token(ttype, value, 0, 0)
        return token
    
    ###### Handles ######

    def handle_accessor(self) -> list:
        """ return two token_type for .first_name """

        str_buffer,ret_tokens=([],[])

        ret_tokens.append(self._create_token(TokenType.DOT))
        self._advance()

        while self._is_identifier(self.current):
            str_buffer.append(self.current)
            self._advance()
        value= ''.join(str_buffer)

        ret_tokens.append(self._create_token(TokenType.ACCESSOR_IDENTIFIER,value))
        return ret_tokens
    
    def handle_identifier(self) -> TokenType:
        """ Return token for first_name: """
        str_buffer = []        
        while self._is_identifier(self.current):
            str_buffer.append(self.current)
            self._advance()
        value= ''.join(str_buffer)
        return self._create_token(TokenType.ACCESSOR_IDENTIFIER,value)

    def skip_comments(self) -> None:
        """ Skips line with comments """
        while not self._is_end():
            if self.current in NEW_LINES:
                break
            self._advance()

    def scan_string(self) -> str:
        """ Scans for a string and returns a string Token """
        ret: list = []
        self._advance() # Start String Scanning
        while not self._is_end():
            c = self.current
            if c == '"': # End of String
                self._advance() # Take out of current string
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
                    msg="Newlines inside string are not allowed",
                    line=self.line,col=self.col
                )
            else:
                ret.append(c)

            self._advance()
            
        raise LexerError(
            msg="Invalid JQ (String must be terminated)",
            line=self.line,col=self.col
        )
    
    def scan_number(self) -> str:
        start_idx = self.current_idx

        # Consume leading '-' if present
        if self.current == "-":
            self._advance()

        # Consume digits
        while self.current is not None and self.current.isdigit():
            self._advance()

        # Consume optional decimal part
        if self.current == ".":
            self._advance()
            while self.current is not None and self.current.isdigit():
                self._advance()

        # Consume optional exponent part
        if self.current is not None and self.current.lower() == "e":
            self._advance()
            # Exponent may have + or -
            if self.current in {"+", "-"}:
                self._advance()
            while self.current is not None and self.current.isdigit():
                self._advance()

        # Extract the raw substring from start_idx to current position
        raw_number = self.program[start_idx:self.current_idx]

        value = None
        if (
            "e" in raw_number.lower() 
            or "E" in raw_number.lower()
        ):
            value = Decimal(raw_number)
        elif "." in raw_number:
            value = float(raw_number)
        else:
            value = int(raw_number)

        return self._create_token(TokenType.NUMBER, value)

    # def scan_variable(self) -> TokenType:

    #     if not self._is_identifier_begin(self._peek()):
    #         raise LexerError(
    #             msg=f"Invalid variable name start - [{self._peek()}]", 
    #             line=self.line, col=self.col
    #         )
        
    #     buf = []
    #     while (
    #         self.current_idx <= self.program_size 
    #         and self._is_ident(self._peek())
    #     ):
    #         buf.append(self._advance())
        
    #     name = ''.join(buf)
    #     return self._create_token(TokenType.VARIABLE, name)
    
    # def scan_identifier_or_keywords(self, first: str) -> Token:
    #     buf = [first]

    #     while (
    #         self.current_idx <= self.program_size
    #         and self._is_ident(self._peek())
    #     ):
    #         buf.append(self._advance())
        
    #     text = ''.join(buf)

    #     ttype = KEYWORDS_MAPPING.get(text)
    #     if ttype is None:
    #         return self._create_token(TokenType.IDENTIFIER, text)
    #     else:
    #         # TODO: Attach semantic value for literals
    #         if ttype is TokenType.NULL:
    #             return self._create_token(TokenType.NULL, None)
    #         if ttype is TokenType.TRUE:
    #             return self._create_token(TokenType.TRUE, True)
    #         if ttype is TokenType.FALSE:
    #             return self._create_token(TokenType.FALSE, False)
            
    #         return self._create_token(ttype, text)
    
    # def _match(self, expected: str) -> bool:
    #     if (
    #         self.current_idx < self.program_size 
    #         and self.program[self.current_idx] == expected
    #     ):
    #         self.current_idx += 1
    #         self.col += 1
    #         return True
    #     return False

    # def scan_operator_or_punct(self, c:str) -> Token | None:
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