WHITE_SPACES = [' ', '\t', '\r']
NEW_LINES = [ "\n", "\r", "\u0085", "\u2028", "\u2029"]

STRING_MAPPING= {
    '"':'"', 
    '\\':'\\', 
    '/':'/',
    'b':'\b', 
    'f':'\f', 
    'n':'\n', 
    'r':'\r', 
    't':'\t'
}

# OPENING_BRACKETS = {
#     str(TokenType.OPEN_PARENTHESIS.value): TokenType.OPEN_PARENTHESIS,
#     str(TokenType.OPEN_CURLY_BRAKET.value): TokenType.OPEN_CURLY_BRAKET,
#     str(TokenType.OPEN_SQUARE_BRACKET.value): TokenType.OPEN_SQUARE_BRACKET
# }

# CLOSING_BRACKETS = {
#     str(TokenType.CLOSE_PARENTHESIS.value): TokenType.CLOSE_PARENTHESIS,
#     str(TokenType.CLOSE_CURLY_BRAKET.value): TokenType.CLOSE_CURLY_BRAKET,
#     str(TokenType.CLOSE_SQUARE_BRACKET.value): TokenType.CLOSE_SQUARE_BRACKET
# }

# KEYWORDS_MAPPING = {
#     TokenType.AS.value: TokenType.AS,
#     TokenType.OR.value: TokenType.OR,
#     TokenType.AND.value: TokenType.AND,
#     TokenType.NOT.value: TokenType.NOT,
#     TokenType.IF.value: TokenType.IF,
#     TokenType.ELSE.value: TokenType.ELSE,
#     TokenType.ELIL.value: TokenType.ELIL,
#     TokenType.THEN.value: TokenType.THEN,
#     TokenType.END.value: TokenType.END,
#     TokenType.NULL.value: TokenType.NULL,
# }

# KEYWORDS_MAPPING = {
#     TokenType.IF.value: TokenType.IF,
#     TokenType.THEN.value: TokenType.THEN,
#     TokenType.ELIL.value: TokenType.ELIL,
#     TokenType.ELSE.value: TokenType.ELSE,
#     TokenType.END.value: TokenType.END,
#     TokenType.AS.value: TokenType.AS,
#     TokenType.AND.value: TokenType.AND,
#     TokenType.OR.value: TokenType.OR,
#     TokenType.NOT.value: TokenType.NOT,
#     TokenType.NULL.value: TokenType.NULL,
#     TokenType.TRY.value: TokenType.TRY,
#     TokenType.CATCH.value: TokenType.CATCH,
#     TokenType.LABEL.value: TokenType.LABEL,
#     TokenType.REDUCE.value: TokenType.REDUCE,
#     TokenType.FOREACH.value: TokenType.FOREACH,
#     TokenType.WHILE.value: TokenType.WHILE,
#     TokenType.UNTIL.value: TokenType.UNTIL, 
#     TokenType.BREAK.value: TokenType.BREAK,
#     TokenType.DEF.value: TokenType.DEF
# }

# OPERATORS = {
#     TokenType.LT.value: TokenType.LT,
#     TokenType.GT.value: TokenType.GT,
#     TokenType.EQ.value: TokenType.EQ,
#     TokenType.NEQ.value: TokenType.NEQ,
#     TokenType.LTE.value: TokenType.LTE,
#     TokenType.GTE.value: TokenType.GTE,
#     TokenType.ALT.value: TokenType.ALT,
#     TokenType.MOD.value: TokenType.MOD,
#     TokenType.DIV.value: TokenType.DIV,
#     TokenType.PIPE.value: TokenType.PIPE,
#     TokenType.PLUS.value: TokenType.PLUS,
#     TokenType.MULT.value: TokenType.MULT,
#     TokenType.COLON.value: TokenType.COLON,
#     TokenType.COMMA.value: TokenType.COMMA,
#     TokenType.MINUS.value: TokenType.MINUS,
#     TokenType.SLASH.value: TokenType.SLASH,
#     TokenType.ASTRICk.value: TokenType.ASTRICk,
#     TokenType.PLUS_EQUL.value: TokenType.PLUS_EQUL,
#     TokenType.DIV_EQUAL.value: TokenType.DIV_EQUAL,
#     TokenType.SEMI_COLON.value: TokenType.SEMI_COLON,
#     TokenType.MULT_EQUAL.value: TokenType.MULT_EQUAL,
#     TokenType.MINUS_EQUAL.value: TokenType.MINUS_EQUAL,
#     TokenType.QUESTION_MARK.value: TokenType.QUESTION_MARK,
# }

# POSSIBLE_ROOTS = [
#     TokenType.AS,
#     TokenType.PIPE,    
#     TokenType.LPAREN,
#     TokenType.LSQRBRC,
#     TokenType.LCURLBRC, 
# ]