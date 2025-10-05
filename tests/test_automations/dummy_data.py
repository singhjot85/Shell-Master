from automations.jq_core.constants import TokenType, Token
from automations.jq_core.ast import *

def create_token(ttype: TokenType, value=None) -> Token:
    """ Create a token given a token_type and value """
    token = None
    if not value:
        token = Token(ttype, ttype.value, 0, 0)
    else:
        token = Token(ttype, value, 0, 0)
    return token

# Type 1
TESTCASES_1 = '.first_name \n .last_name'
TESTCASES_2 = ','
TESTCASES_3 = '.'
TESTCASES_4 = '|'
TESTCASES_5 = '$SomeName'
TESTCASES_6 = 'firstName: "Hello",'
TESTCASES_7 = '_last_name: "World",'
TESTCASES_8 = 'int: 123,'
TESTCASES_9 = 'float: 34.56,'
TESTCASES_10 = 'exp: 234e4,'
TESTCASES_11 = 'negative: -235e4,'
TESTCASES_12 = 'money: $bankBalance,'
TESTCASES_13 = 'if .a then .b else .c end'

# Type 2
TESTCASES_14 = '.first_name[] | { }'
TESTCASES_15 = '.last_name[ if .name | select(.key) then .pmt end ] | { }'
TESTCASES_16 = '("2445") as $bankBalance1 | '
TESTCASES_17 = '.first_name[] | { firstName: "Hello", }'

TESTCASE_RESULTS_TYPE_1 = {
    TESTCASES_1: [
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, "first_name"),
        create_token(TokenType.DOT),
        create_token(TokenType.ACCESSOR_IDENTIFIER, "last_name")
    ],
    TESTCASES_2: [create_token(TokenType.COMMA)],
    TESTCASES_3: [create_token(TokenType.DOT)],
    TESTCASES_4: [create_token(TokenType.PIPE)],
    TESTCASES_5: [
        create_token(TokenType.DOLLAR),
        create_token(TokenType.VARIABLE, "SomeName")
    ],
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
        create_token(TokenType.DOLLAR),
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
}

TESTCASE_RESULTS_TYPE_2 ={
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

# Complete Program
COMPLETE_PROGRAM_1 = ''''
(
    ("2445")  as $bankBalance |
    ("2445") as $bankBalance1 | 
    .first_name[] | {
        firstName: "Hello",
        _last_name: "World",
        int: 123,
        float: 34.56,
        exp: 234e4,
        negative: -235e4,
        money: $bankBalance,
    },
    .last_name[ if .name | select(.key) then .pmt end ] | {
        firstName1: "Hello1",
        _last_name1: "World1",
        int1: 1231,
        float1: 34.561,
        exp1: 1234e4,
        negative1: -1235e4,
        money1: $bankBalance1,
    }
)
'''
COMPLETE_PROGRAM_2 = """
def addmul(a; b): (a + b) * (a - b);
("12") as $input | 
$input | addmul(5; .value) | {result: ., double: (. * 2)}
"""
COMPLETE_PROGRAM_3 = """
if .age >= 18 then "adult"
elif .age >= 13 then "teenager"
else "child"
end
"""
COMPLETE_PROGRAM_4 = """
.people[]
| select(.active == true)
| {name, emails: [.contacts[]?.email // "unknown"]}
"""
COMPLETE_PROGRAM_5 = """
def greet(name): "Hello, \(name)! Today is \(now | strftime("%A")).";
greet(.username)
"""
COMPLETE_PROGRAM_6 = """
reduce range(0; 10) as $i (0;
  . + (if ($i % 2 == 0) then $i else 0 end)
)
| select(. > 10 and . < 30)
"""

TESTCASE_RESULTS_COMPLETE_PROGRAMS = {
    # Using print statement ouptut as writing entire token stream is painful
    COMPLETE_PROGRAM_1: "[<Token TokenType.LPAREN - '('>, <Token TokenType.LPAREN - '('>, <Token TokenType.STRING - '2445'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.AS - 'as'>, <Token TokenType.DOLLAR - '$'>, <Token TokenType.VARIABLE - 'bankBalance'>, <Token TokenType.PIPE - '|'>, <Token TokenType.LPAREN - '('>, <Token TokenType.STRING - '2445'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.AS - 'as'>, <Token TokenType.DOLLAR - '$'>, <Token TokenType.VARIABLE - 'bankBalance1'>, <Token TokenType.PIPE - '|'>, <Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'first_name'>, <Token TokenType.LSQRBRC - '['>, <Token TokenType.RSQRBRC - ']'>, <Token TokenType.PIPE - '|'>, <Token TokenType.LCURLBRC - '{'>, <Token TokenType.IDENTIFIER - 'firstName'>, <Token TokenType.COLON - ':'>, <Token TokenType.STRING - 'Hello'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - '_last_name'>, <Token TokenType.COLON - ':'>, <Token TokenType.STRING - 'World'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - 'int'>, <Token TokenType.COLON - ':'>, <Token TokenType.NUMBER - '123'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - 'float'>, <Token TokenType.COLON - ':'>, <Token TokenType.NUMBER - '34.56'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - 'exp'>, <Token TokenType.COLON - ':'>, <Token TokenType.NUMBER - '2.34E+6'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - 'negative'>, <Token TokenType.COLON - ':'>, <Token TokenType.NUMBER - '-2.35E+6'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - 'money'>, <Token TokenType.COLON - ':'>, <Token TokenType.DOLLAR - '$'>, <Token TokenType.VARIABLE - 'bankBalance'>, <Token TokenType.COMMA - ','>, <Token TokenType.RCURLBRC - '}'>, <Token TokenType.COMMA - ','>, <Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'last_name'>, <Token TokenType.LSQRBRC - '['>, <Token TokenType.IF - 'if'>, <Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'name'>, <Token TokenType.PIPE - '|'>, <Token TokenType.IDENTIFIER - 'select'>, <Token TokenType.LPAREN - '('>, <Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'key'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.THEN - 'then'>, <Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'pmt'>, <Token TokenType.END - 'end'>, <Token TokenType.RSQRBRC - ']'>, <Token TokenType.PIPE - '|'>, <Token TokenType.LCURLBRC - '{'>, <Token TokenType.IDENTIFIER - 'firstName1'>, <Token TokenType.COLON - ':'>, <Token TokenType.STRING - 'Hello1'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - '_last_name1'>, <Token TokenType.COLON - ':'>, <Token TokenType.STRING - 'World1'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - 'int1'>, <Token TokenType.COLON - ':'>, <Token TokenType.NUMBER - '1231'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - 'float1'>, <Token TokenType.COLON - ':'>, <Token TokenType.NUMBER - '34.561'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - 'exp1'>, <Token TokenType.COLON - ':'>, <Token TokenType.NUMBER - '1.234E+7'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - 'negative1'>, <Token TokenType.COLON - ':'>, <Token TokenType.NUMBER - '-1.235E+7'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - 'money1'>, <Token TokenType.COLON - ':'>, <Token TokenType.DOLLAR - '$'>, <Token TokenType.VARIABLE - 'bankBalance1'>, <Token TokenType.COMMA - ','>, <Token TokenType.RCURLBRC - '}'>, <Token TokenType.RPAREN - ')'>]",
    COMPLETE_PROGRAM_2: "[<Token TokenType.DEF - 'def'>, <Token TokenType.IDENTIFIER - 'addmul'>, <Token TokenType.LPAREN - '('>, <Token TokenType.IDENTIFIER - 'a'>, <Token TokenType.SEMI_COLON - ';'>, <Token TokenType.IDENTIFIER - 'b'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.COLON - ':'>, <Token TokenType.LPAREN - '('>, <Token TokenType.IDENTIFIER - 'a'>, <Token TokenType.PLUS - '+'>, <Token TokenType.IDENTIFIER - 'b'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.ASTRICk - '*'>, <Token TokenType.LPAREN - '('>, <Token TokenType.IDENTIFIER - 'a'>, <Token TokenType.MINUS - '-'>, <Token TokenType.IDENTIFIER - 'b'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.SEMI_COLON - ';'>, <Token TokenType.LPAREN - '('>, <Token TokenType.STRING - '12'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.AS - 'as'>, <Token TokenType.DOLLAR - '$'>, <Token TokenType.VARIABLE - 'input'>, <Token TokenType.PIPE - '|'>, <Token TokenType.DOLLAR - '$'>, <Token TokenType.VARIABLE - 'input'>, <Token TokenType.PIPE - '|'>, <Token TokenType.IDENTIFIER - 'addmul'>, <Token TokenType.LPAREN - '('>, <Token TokenType.NUMBER - '5'>, <Token TokenType.SEMI_COLON - ';'>, <Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'value'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.PIPE - '|'>, <Token TokenType.LCURLBRC - '{'>, <Token TokenType.IDENTIFIER - 'result'>, <Token TokenType.COLON - ':'>, <Token TokenType.DOT - '.'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - 'double'>, <Token TokenType.COLON - ':'>, <Token TokenType.LPAREN - '('>, <Token TokenType.DOT - '.'>, <Token TokenType.ASTRICk - '*'>, <Token TokenType.NUMBER - '2'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.RCURLBRC - '}'>]",
    COMPLETE_PROGRAM_3: "[<Token TokenType.IF - 'if'>, <Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'age'>, <Token TokenType.GT - '>'>, <Token TokenType.NUMBER - '18'>, <Token TokenType.THEN - 'then'>, <Token TokenType.STRING - 'adult'>, <Token TokenType.ELIL - 'elif'>, <Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'age'>, <Token TokenType.GT - '>'>, <Token TokenType.NUMBER - '13'>, <Token TokenType.THEN - 'then'>, <Token TokenType.STRING - 'teenager'>, <Token TokenType.ELSE - 'else'>, <Token TokenType.STRING - 'child'>, <Token TokenType.END - 'end'>]",
    COMPLETE_PROGRAM_4: "[<Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'people'>, <Token TokenType.LSQRBRC - '['>, <Token TokenType.RSQRBRC - ']'>, <Token TokenType.PIPE - '|'>, <Token TokenType.IDENTIFIER - 'select'>, <Token TokenType.LPAREN - '('>, <Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'active'>, <Token TokenType.IDENTIFIER - 'true'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.PIPE - '|'>, <Token TokenType.LCURLBRC - '{'>, <Token TokenType.IDENTIFIER - 'name'>, <Token TokenType.COMMA - ','>, <Token TokenType.IDENTIFIER - 'emails'>, <Token TokenType.COLON - ':'>, <Token TokenType.LSQRBRC - '['>, <Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'contacts'>, <Token TokenType.LSQRBRC - '['>, <Token TokenType.RSQRBRC - ']'>, <Token TokenType.QUESTION_MARK - '?'>, <Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'email'>, <Token TokenType.ALT - '//'>, <Token TokenType.STRING - 'unknown'>, <Token TokenType.RSQRBRC - ']'>, <Token TokenType.RCURLBRC - '}'>]",
    COMPLETE_PROGRAM_5: "[<Token TokenType.DEF - 'def'>, <Token TokenType.IDENTIFIER - 'greet'>, <Token TokenType.LPAREN - '('>, <Token TokenType.IDENTIFIER - 'name'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.COLON - ':'>, <Token TokenType.STRING - 'Hello, name)! Today is now | strftime('>, <Token TokenType.MOD - '%'>, <Token TokenType.IDENTIFIER - 'A'>, <Token TokenType.STRING - ')).'>, <Token TokenType.SEMI_COLON - ';'>, <Token TokenType.IDENTIFIER - 'greet'>, <Token TokenType.LPAREN - '('>, <Token TokenType.DOT - '.'>, <Token TokenType.ACCESSOR_IDENTIFIER - 'username'>, <Token TokenType.RPAREN - ')'>]",
    COMPLETE_PROGRAM_6: "[<Token TokenType.REDUCE - 'reduce'>, <Token TokenType.IDENTIFIER - 'range'>, <Token TokenType.LPAREN - '('>, <Token TokenType.NUMBER - 'NUMBER'>, <Token TokenType.SEMI_COLON - ';'>, <Token TokenType.NUMBER - '10'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.AS - 'as'>, <Token TokenType.DOLLAR - '$'>, <Token TokenType.VARIABLE - 'i'>, <Token TokenType.LPAREN - '('>, <Token TokenType.NUMBER - 'NUMBER'>, <Token TokenType.SEMI_COLON - ';'>, <Token TokenType.DOT - '.'>, <Token TokenType.PLUS - '+'>, <Token TokenType.LPAREN - '('>, <Token TokenType.IF - 'if'>, <Token TokenType.LPAREN - '('>, <Token TokenType.DOLLAR - '$'>, <Token TokenType.VARIABLE - 'i'>, <Token TokenType.MOD - '%'>, <Token TokenType.NUMBER - '2'>, <Token TokenType.NUMBER - 'NUMBER'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.THEN - 'then'>, <Token TokenType.DOLLAR - '$'>, <Token TokenType.VARIABLE - 'i'>, <Token TokenType.ELSE - 'else'>, <Token TokenType.NUMBER - 'NUMBER'>, <Token TokenType.END - 'end'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.RPAREN - ')'>, <Token TokenType.PIPE - '|'>, <Token TokenType.IDENTIFIER - 'select'>, <Token TokenType.LPAREN - '('>, <Token TokenType.DOT - '.'>, <Token TokenType.GT - '>'>, <Token TokenType.NUMBER - '10'>, <Token TokenType.AND - 'and'>, <Token TokenType.DOT - '.'>, <Token TokenType.LT - '<'>, <Token TokenType.NUMBER - '30'>, <Token TokenType.RPAREN - ')'>]"
}