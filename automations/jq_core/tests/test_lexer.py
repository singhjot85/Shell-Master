""" Pytests to insure Lexer stays intact """
from automations.jq_core.lexer import Lexer
from automations.jq_core.constants import TokenType, Token


def create_token(ttype: TokenType, value=None) -> Token:
    """ Create a token given a token_type and value """
    token = None
    if not value:
        token = Token(ttype, ttype.value, 0, 0)
    else:
        token = Token(ttype, value, 0, 0)
    return token

TESTCASES_1 = '.first_name \n .last_name'
TESTCASES_2 = ','
TESTCASES_3 = '.'
TESTCASES_4 = '|'
TESTCASES_5 = '$'
TESTCASES_6 = 'firstName: "Hello",'
TESTCASES_7 = '_last_name: "World",'
TESTCASES_8 = 'int: 123,'
TESTCASES_9 = 'float: 34.56,'
TESTCASES_10 = 'exp: 234e4,'
TESTCASES_11 = 'negative: -235e4,'
TESTCASES_12 = 'money: $bankBalance,'
TESTCASES_13 = 'if .a then .b else .c end'
TESTCASES_14 = '.first_name[] | { }'
TESTCASES_15 = '.last_name[ if .name | select(.key) then .pmt end ] | { }'
TESTCASES_16 = '("2445") as $bankBalance1 | '
TESTCASES_17 = '.first_name[] | { firstName: "Hello", }'

TESTCASE_RESULTS = {
    TESTCASES_1: [
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, "first_name"),
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, "last_name")
    ],
    TESTCASES_2: [create_token(TokenType.COMMA)],
    TESTCASES_3: [create_token(TokenType.DOT)],
    TESTCASES_4: [create_token(TokenType.PIPE)],
    TESTCASES_5: [create_token(TokenType.DOLLAR)],
    TESTCASES_6: [
        create_token(TokenType.IDENTIFIER, "firstName"),
        create_token(TokenType.COLON),
        create_token(TokenType.STRING, "Hello"),
        create_token(TokenType.COMMA),
    ],
    TESTCASES_7: [
        create_token(TokenType.IDENTIFIER, "_last_name"),
        create_token(TokenType.COLON),
        create_token(TokenType.STRING, "World"),
        create_token(TokenType.COMMA),
    ],
    TESTCASES_8: [
        create_token(TokenType.IDENTIFIER, "int"),
        create_token(TokenType.COLON),
        create_token(TokenType.NUMBER, 123),
        create_token(TokenType.COMMA),
    ],
    TESTCASES_9: [
        create_token(TokenType.IDENTIFIER, "float"),
        create_token(TokenType.COLON),
        create_token(TokenType.NUMBER, 34.56),
        create_token(TokenType.COMMA),
    ],
    TESTCASES_10: [
        create_token(TokenType.IDENTIFIER, "exp"),
        create_token(TokenType.COLON),
        create_token(TokenType.NUMBER, 234e4),
        create_token(TokenType.COMMA),
    ],
    TESTCASES_11: [
        create_token(TokenType.IDENTIFIER, "negative"),
        create_token(TokenType.COLON),
        create_token(TokenType.NUMBER, -235e4),
        create_token(TokenType.COMMA),
    ],
    TESTCASES_12: [
        create_token(TokenType.IDENTIFIER, "money"),
        create_token(TokenType.COLON),
        create_token(TokenType.VARIABLE, "bankBalance"),
        create_token(TokenType.COMMA),
    ],
    TESTCASES_13: [
        create_token(TokenType.IF),
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, 'a'),
        create_token(TokenType.THEN),
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, 'b'),
        create_token(TokenType.ELSE),
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, 'c'),
        create_token(TokenType.END)
    ],
    TESTCASES_14: [
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, 'first_name'),
        create_token(TokenType.LSQRBRC),
        create_token(TokenType.RSQRBRC),
        create_token(TokenType.PIPE),
        create_token(TokenType.LPAREN),
        create_token(TokenType.RPAREN)
    ],
    TESTCASES_15: [
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, "last_name"),
        create_token(TokenType.LSQRBRC),
        create_token(TokenType.IF),
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, "name"),
        create_token(TokenType.PIPE),
        create_token(TokenType.IDENTIFIER, "select"), # TODO: Change this when handling is added
        create_token(TokenType.LPAREN),
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, 'key'),
        create_token(TokenType.RPAREN),
        create_token(TokenType.THEN),
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, "pmt"),
        create_token(TokenType.END),
        create_token(TokenType.RSQRBRC),
        create_token(TokenType.PIPE),
        create_token(TokenType.LCURLBRC),
        create_token(TokenType.RCURLBRC)
    ],
    TESTCASES_16: [
        create_token(TokenType.LPAREN),
        create_token(TokenType.STRING, "2445"),
        create_token(TokenType.RPAREN),
        create_token(TokenType.AS),
        create_token(TokenType.DOLLAR),
        create_token(TokenType.VARIABLE, 'bankBalance1'),
        create_token(TokenType.PIPE)
    ],
    TESTCASES_17: [
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, "first_name"),
        create_token(TokenType.LPAREN),
        create_token(TokenType.RPAREN),
        create_token(TokenType.PIPE),
        create_token(TokenType.LCURLBRC),
        create_token(TokenType.IDENTIFIER, "firstName"),
        create_token(TokenType.COLON),
        create_token(TokenType.STRING, "Hello"),
        create_token(TokenType.COMMA),
        create_token(TokenType.RCURLBRC)
    ],
}
class TestBasicLexing:
    
    def test_operators(self):
        for program in TESTCASE_RESULTS:
            tokens = Lexer(program).tokenize()

            assert isinstance(tokens, list) == True
            assert len(tokens) == len(TESTCASE_RESULTS[program])
            assert tokens == TESTCASE_RESULTS[program]
        