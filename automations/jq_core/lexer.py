from decimal import Decimal
from .utils import JQUtils
from .input import StringInputHandler, BytesInputHandler
from .constants import STRING_MAPPING, WHITE_SPACES, NEW_LINES
from . import (
    Token, 
    TokenType, 
    Keywords,
    Identifiers,
    Literals,
    Operators,
    Delimiters,
)

class Lexer:
    """ Implements the algorithm for lexical analyzer """

    def __init__(self, source: str):
        """ keeping the logic of lines and columns as we need it in debugger """
        self.handler = None
        if isinstance(source, str):
            self.handler: StringInputHandler = StringInputHandler(source)
        elif isinstance(source, (bytes, bytearray)):
            self.handler: BytesInputHandler = BytesInputHandler(source)

    def tokenize(self) -> list[Token] | list:
        try:
            tokens = []
            while (
                not self.handler.eof()
                and (char := self.handler.char)
            ):
                next_char = self.handler.peek()
                if(
                    char in WHITE_SPACES
                    or char in NEW_LINES
                    or char == Delimiters.HASH.value
                ):
                    self.handler.next()
                    continue

                if char == Delimiters.DOLLAR.value:
                    tokens.append(self._scan_variable())
                    continue
                if char == Delimiters.DOT.value:
                    tokens.append(self._scan_access_variable())
                    continue
                if char == Delimiters.DOUBLE_QOUTES.value:
                    tokens.append(self._scan_string())
                    continue
                if JQUtils.is_valid_identifier(char, True):
                    tokens.append(self._scan_identifiers())
                    continue
                if JQUtils.is_valid_number(char, next_char):
                    tokens.append(self._scan_number())
                    continue

                type, value, category = (None, None, None)
                if char in Delimiters._value2member_map_:
                    category = Delimiters.__name__
                    type = Delimiters(char).name
                    value = Delimiters(char).value
                if char in Operators._value2member_map_ :
                    category = Operators.__name__
                    type = Operators(char).name
                    value = Operators(char).value
                if (
                    next_char 
                    and (
                        (operator := ''.join([char,next_char]) ) 
                        in Operators._value2member_map_
                    )
                ):
                    category = Operators.__name__
                    type = Operators(operator).name
                    value = Operators(operator).value
                    self.handler.next()
                if type or value or category:
                    tokens.append(JQUtils.create_token(
                        category,
                        type,
                        value,
                        self.handler 
                    ))
                    self.handler.next()
            return tokens
        # except JQException as exc:
        except Exception as exc:
            raise exc

    def _scan_variable(self) -> Token:
        """Scan of JQ variables: $varName234 
        Possiblities: $[A-Za-z_][A-Za-z0-9_]
        """
        self.handler.next()
        if not self.handler.char:
            err_str = "Invalid Variable Name"
            raise Exception(err_str)
        token:Token = self._scan_identifiers()
        token.type = Identifiers.VARIAVBLE.name
        token.value = ''.join(['$',token.value])
        return token

    def _scan_access_variable(self) -> Token:
        """Scan Access Variable in JQ
        Possibilities:
            - .[A-Za-z_][A-Za-z0-9_]
            - ."..."
            - .["..."]
        ... -> can be any character
        """
        self.handler.next()
        if not self.handler.char:
            err_str = "Invalid Variable Name"
            raise Exception(err_str)
        
        value = None
        if self.handler.char == Delimiters.OPEN_SQUARE_BRACKET.value:
            # Variable is .["foo-@bar"]
            buf = ['.', '[', self._scan_string().value, ']']
            value = ''.join(buf)
        if self.handler.char == Delimiters.DOUBLE_QOUTES.value:
            # Variable is ."foo-@bar"
            value = ''.join(['.', self._scan_string().value])
        
        value = ''.join(['.',self._scan_identifiers().value])
        
        return JQUtils.create_token(
            Identifiers.__name__,
            Identifiers.ACCESS_VARIABLE.value,
            value,
            self.handler
        )

    def _scan_string(self) -> Token:
        """Scans for a string and returns a string Token"""
        ret: list = ['"']
        self.handler.next() # Start String Scanning
        while not self.handler.eof():
            c = self.handler.char
            if c == '"': # End of String
                self.handler.next() # Take out of current string
                ret.append('"')
                return JQUtils.create_token(
                    Literals.__name__,
                    Literals.STRING.name,
                    ''.join(ret),
                    self.handler
                )
            
            if c == "\\":
                esc = self.handler.next()
                if esc in '"\\/bfnrt':
                    ret.append(STRING_MAPPING[esc])
                elif esc == "u": # Read exactly 4 hex digits
                    hex_digits = [self.handler.next() for _ in range(4)]
                    if not all(d.lower() in '0123456789abcdef' for d in hex_digits): 
                        Exception(msg="Invalid \\u escape")
                    codepoint = int(''.join(hex_digits), 16)
                    ret.append(chr(codepoint))
            elif c == '\n': # Newline inside stings
                line, col, _ = self.handler.position()
                raise Exception("Newlines inside string are not allowed")
            else:
                ret.append(c)

            self.handler.next()
        raise Exception("Unterminated String detected")
        # line, col, _ = self.handler.position()
        # raise LexerError(
        #     msg="Invalid JQ (String must be terminated)",
        #     line=line, col=col
        # )

    def _scan_number(self) -> Token:
        start_idx = self.handler.index

        # Consume leading '-' if present
        if self.handler.char == "-":
            self.handler.next()

        # Consume digits
        while self.handler.char is not None and self.handler.char.isdigit():
            self.handler.next()

        # Consume optional decimal part
        if self.handler.char == ".":
            self.handler.next()
            while self.handler.char is not None and self.handler.char.isdigit():
                self.handler.next()

        # Consume optional exponent part
        if self.handler.char is not None and self.handler.char.lower() == "e":
            self.handler.next()
            # Exponent may have + or -
            if self.handler.char in {"+", "-"}:
                self.handler.next()
            while self.handler.char is not None and self.handler.char.isdigit():
                self.handler.next()

        # Extract the raw substring from start_idx to current position
        raw_number = self.handler.text[start_idx:self.handler.index]

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

        return JQUtils.create_token(
            Literals.__name__,
            Literals.NUMBER.value,
            value,
            self.handler
        )

    def _scan_identifiers(self) -> TokenType:
        """Scans a valid Identifiers
        Possibilites:
            - Starts with [A-Za-z_]
            - Else [A-Z0-9a-z_]
        """
        buffer = [self.handler.char]
        self.handler.next()
        
        while (
            not self.handler.eof()
            and (char := self.handler.char)
            and JQUtils.is_valid_identifier(char) 
        ):
            buffer.append(char)
            self.handler.next()

        category = Identifiers.__name__
        # type can be Identifiers.FUNCTION as that's the only one not covered yet
        type = category 
        value = ''.join(buffer)

        if value in Keywords._value2member_map_:
            category = Keywords.__name__
            type = Keywords(value).name
            value = Keywords(value).value

        return JQUtils.create_token(
            category,
            type,
            value,
            self.handler
        )

# class LexerExtended(Lexer):
#     """
#     A stack based approch that gives nested objects in a list of tokens
#     Needs bug-fixes and is increasing complexity, 
#     The base lexer should work fine for all usecases.
#     """
#     def __init__(self, source):
#         super().__init__(source)
    
#     def _is_same_set(self, key: str) -> bool:
#         """ Return if the key(given) and self.handler.char are of same set """
#         if not key:
#             return False
        
#         if key in OPENING_BRACKETS:
#             if key == TokenType.LPAREN.value:
#                 return self.handler.char == TokenType.RPAREN.value
#             if key == TokenType.LSQRBRC.value:
#                 return self.handler.char == TokenType.RSQRBRC.value
#             if key == TokenType.LCURLBRC.value:
#                 return self.handler.char == TokenType.RCURLBRC.value
#         if key in CLOSING_BRACKETS:
#             if key == TokenType.RPAREN.value:
#                 return self.handler.char == TokenType.LPAREN.value
#             if key == TokenType.RSQRBRC.value:
#                 return self.handler.char == TokenType.LSQRBRC.value
#             if key == TokenType.RCURLBRC.value:
#                 return self.handler.char == TokenType.LCURLBRC.value

#         return False

#     def _lexit(self, start_idx:int) -> list[TokenType]:
#         """ Lexical Analyze a given program, start index is required. """
#         sub_program = self.handler.text[start_idx:self.handler.index]
#         lexer: Lexer = Lexer(sub_program)
#         sub_tokens: list[TokenType] = lexer.tokenize()
#         del lexer
#         return sub_tokens

#     def _peep_last_tuple(self, stack: list = []) -> list[tuple[Token,int]] | None:
#         """ Special peep method to peep JQ lexer stack """
#         top_tuple = None

#         if stack[-1] and isinstance(stack[-1], tuple):
#             top_tuple = stack[-1]
#         else:
#             for item in reversed(stack):
#                 if isinstance(item, tuple):
#                     top_tuple = item

#         return top_tuple

#     def handle_brackets(self) -> list:
#         """
#         Recurive lexer to make things easier for parser.
#         Returns:
#             result (list): List of Tokens in format:
#                 [TokenType.RSQRBRC,list[Tokens],TokenType.LSQRBRC]
#         """
#         if self.handler.char not in OPENING_BRACKETS:
#             LexerError(
#                 msg="Mismatching Brackets",
#                 line=self.line,col=self.col
#             )

#         stack: list[tuple[Token,int]] | list[list] | int= []
#         while not self.handler.eof():
#             if self.handler.char in OPENING_BRACKETS:
#                 if stack:
#                     if not isinstance(stack[-1], int):
#                         prev_start_idx = self._peep_last_tuple(stack)[1] + 1
#                     else:
#                         prev_start_idx = stack.pop()
                        
#                     if prev_start_idx is None:
#                         raise LexerError(msg="Error occurred in recursion",line=self.line, col=self.col)
#                     if tokens:=self._lexit(prev_start_idx):
#                         tokens: list[TokenType]
#                         stack.append(tokens)

#                 opening_brac: tuple[TokenType, int] = (
#                     self.create_token(OPENING_BRACKETS[self.handler.char]), 
#                     self.handler.index
#                 )
#                 stack.append(opening_brac)
#                 self.handler.next()
#                 continue
#             if self.handler.char in CLOSING_BRACKETS:
#                 top_tuple: tuple[Token,int] = self._peep_last_tuple(stack)
#                 if (
#                     not self._is_same_set(top_tuple[0].value)
#                     or not top_tuple
#                 ):
#                     line, col, _ = self.handler.position()
#                     raise LexerError(msg="Imbalanced Brackets", line=line, col=col)
                
#                 prev_start_idx = top_tuple[1] + 1
#                 if prev_start_idx is None:
#                     raise LexerError(msg="Error occurred in recursion",line=self.line, col=self.col)
#                 if tokens:=self._lexit(prev_start_idx):
#                     tokens: list[TokenType]
#                     stack.append(tokens)
                
#                 temp_list: list[Token | list]= []
#                 while stack[-1] and not isinstance(stack[-1], tuple):
#                     temp_list.extend(stack.pop())
                
#                 closing_brac = [stack.pop()[0]]
#                 if temp_list:
#                     closing_brac.append(temp_list)
#                 closing_brac.append(self.create_token(CLOSING_BRACKETS[self.handler.char]))
#                 stack.append(closing_brac)

#                 self.handler.next()
#                 continue
#             self.handler.next()
        
#         return stack