from automations.jq_core.ast import *

INPUT_TYPE_1 = {
    "TESTCASE_2": ',',
    "TESTCASE_1": '.first_name \n .last_name',
    "TESTCASE_3": '.name',
    "TESTCASE_4": '|',
    "TESTCASE_5": '$SomeName',
    "TESTCASE_6": 'firstName: "Hello",',
    "TESTCASE_7": '_last_name: "World",',
    "TESTCASE_8": 'int: 123,',
    "TESTCASE_9": 'float: 34.56,',
    "TESTCASE_10": 'exp: 234e4,',
    "TESTCASE_11": 'negative: -235e4,',
    "TESTCASE_12": 'money: $bankBalance,',
    "TESTCASE_13": 'if .a then .b else .c end',
    "TESTCASE_14": '.first_name[] | { }',
    "TESTCASE_15": '.last_name[ if .name | select(.key) then .pmt end ] | { }',
    "TESTCASE_16": '("2445") as $bankBalance1 | ',
    "TESTCASE_17": '.first_name[] | { firstName: "Hello", }'
}

RESULT_TYPE_1 = {
    "TESTCASE_1": """[<Token access_variable - '.first_name'>, <Token access_variable - '.last_name'>]""",
    "TESTCASE_2": """[<Token COMMA - ','>]""",
    "TESTCASE_3": """[<Token access_variable - '.name'>]""",
    "TESTCASE_4": """[<Token PIPE - '|'>]""",
    "TESTCASE_5": """[<Token VARIAVBLE - '$SomeName'>]""",
    "TESTCASE_6": """[<Token mapping_key - 'firstName:'>, <Token STRING - '"Hello"'>, <Token COMMA - ','>]""",
    "TESTCASE_7": """[<Token mapping_key - '_last_name:'>, <Token STRING - '"World"'>, <Token COMMA - ','>]""",
    "TESTCASE_8": """[<Token mapping_key - 'int:'>, <Token number - '123'>, <Token COMMA - ','>]""",
    "TESTCASE_9": """[<Token mapping_key - 'float:'>, <Token number - '34.56'>, <Token COMMA - ','>]""",
    "TESTCASE_10": """[<Token mapping_key - 'exp:'>, <Token number - '2.34E+6'>, <Token COMMA - ','>]""",
    "TESTCASE_11": """[<Token mapping_key - 'negative:'>, <Token number - '-2.35E+6'>, <Token COMMA - ','>]""",
    "TESTCASE_12": """[<Token mapping_key - 'money:'>, <Token VARIAVBLE - '$bankBalance'>, <Token COMMA - ','>]""",
    "TESTCASE_13": """[<Token IF - 'if'>, <Token access_variable - '.a'>, <Token THEN - 'then'>, <Token access_variable - '.b'>, <Token ELSE - 'else'>, <Token access_variable - '.c'>, <Token END - 'end'>]""",
    "TESTCASE_14": """[<Token access_variable - '.first_name'>, <Token OPEN_SQUARE_BRACKET - '['>, <Token CLOSE_SQUARE_BRACKET - ']'>, <Token PIPE - '|'>, <Token OPEN_CURLY_BRAKET - '{'>, <Token CLOSE_CURLY_BRAKET - '}'>]""",
    "TESTCASE_15": """[<Token access_variable - '.last_name'>, <Token OPEN_SQUARE_BRACKET - '['>, <Token IF - 'if'>, <Token access_variable - '.name'>, <Token PIPE - '|'>, <Token Identifiers - 'select'>, <Token OPEN_PARENTHESIS - '('>, <Token access_variable - '.key'>, <Token CLOSE_PARENTHESIS - ')'>, <Token THEN - 'then'>, <Token access_variable - '.pmt'>, <Token END - 'end'>, <Token CLOSE_SQUARE_BRACKET - ']'>, <Token PIPE - '|'>, <Token OPEN_CURLY_BRAKET - '{'>, <Token CLOSE_CURLY_BRAKET - '}'>]""",
    "TESTCASE_16": """[<Token OPEN_PARENTHESIS - '('>, <Token STRING - '"2445"'>, <Token CLOSE_PARENTHESIS - ')'>, <Token AS - 'as'>, <Token VARIAVBLE - '$bankBalance1'>, <Token PIPE - '|'>]""",
    "TESTCASE_17": """[<Token access_variable - '.first_name'>, <Token OPEN_SQUARE_BRACKET - '['>, <Token CLOSE_SQUARE_BRACKET - ']'>, <Token PIPE - '|'>, <Token OPEN_CURLY_BRAKET - '{'>, <Token mapping_key - 'firstName:'>, <Token STRING - '"Hello"'>, <Token COMMA - ','>, <Token CLOSE_CURLY_BRAKET - '}'>]"""
}

COMPLETE_PROGRAMS = {
    "COMPLETE_PROGRAM_1": """( ("2445")  as $bankBalance | ("2445") as $bankBalance1 | .first_name[] | {firstName: "Hello",_last_name: "World",int: 123,float: 34.56,exp: 234e4,negative: -235e4,money: $bankBalance, }, .last_name[ if .name | select(.key) then .pmt end ] | {firstName1: "Hello1",_last_name1: "World1",int1: 1231,float1: 34.561,exp1: 1234e4,negative1: -1235e4,money1: $bankBalance1,})""",
    "COMPLETE_PROGRAM_2": """def addmul(a; b): (a + b) * (a - b); ("12") as $input | $input | addmul(5; .value) | {result: ., double: (. * 2)}""",
    "COMPLETE_PROGRAM_3": """if .age >= 18 then "adult" elif .age >= 13 then "teenager" else "child" end""",
    "COMPLETE_PROGRAM_4": """.people[] | select(.active == true) | {name, emails: [.contacts[]?.email // "unknown"]}""",
    "COMPLETE_PROGRAM_5": """def greet(name): "Hello, \(name)! Today is \(now | strftime("%A"))."; greet(.username)"""
}
# TODO: Handle cases where numbers are directly present in program. Ex: 0, -2.3
# COMPLETE_PROGRAM_6 = """
# reduce range(0; 10) as $i (0;
#   . + (if ($i % 2 == 0) then $i else 0 end)
# )
# | select(. > 10 and . < 30)
# """

# Using print statement ouptut as writing entire token stream is painful
COMPLETE_PROGRAMS_RESULTS = { 
    "COMPLETE_PROGRAM_1": """[<Token OPEN_PARENTHESIS - '('>, <Token OPEN_PARENTHESIS - '('>, <Token STRING - '"2445"'>, <Token CLOSE_PARENTHESIS - ')'>, <Token AS - 'as'>, <Token VARIAVBLE - '$bankBalance'>, <Token PIPE - '|'>, <Token OPEN_PARENTHESIS - '('>, <Token STRING - '"2445"'>, <Token CLOSE_PARENTHESIS - ')'>, <Token AS - 'as'>, <Token VARIAVBLE - '$bankBalance1'>, <Token PIPE - '|'>, <Token access_variable - '.first_name'>, <Token OPEN_SQUARE_BRACKET - '['>, <Token CLOSE_SQUARE_BRACKET - ']'>, <Token PIPE - '|'>, <Token OPEN_CURLY_BRAKET - '{'>, <Token mapping_key - 'firstName:'>, <Token STRING - '"Hello"'>, <Token COMMA - ','>, <Token mapping_key - '_last_name:'>, <Token STRING - '"World"'>, <Token COMMA - ','>, <Token mapping_key - 'int:'>, <Token number - '123'>, <Token COMMA - ','>, <Token mapping_key - 'float:'>, <Token number - '34.56'>, <Token COMMA - ','>, <Token mapping_key - 'exp:'>, <Token number - '2.34E+6'>, <Token COMMA - ','>, <Token mapping_key - 'negative:'>, <Token number - '-2.35E+6'>, <Token COMMA - ','>, <Token mapping_key - 'money:'>, <Token VARIAVBLE - '$bankBalance'>, <Token COMMA - ','>, <Token CLOSE_CURLY_BRAKET - '}'>, <Token COMMA - ','>, <Token access_variable - '.last_name'>, <Token OPEN_SQUARE_BRACKET - '['>, <Token IF - 'if'>, <Token access_variable - '.name'>, <Token PIPE - '|'>, <Token Identifiers - 'select'>, <Token OPEN_PARENTHESIS - '('>, <Token access_variable - '.key'>, <Token CLOSE_PARENTHESIS - ')'>, <Token THEN - 'then'>, <Token access_variable - '.pmt'>, <Token END - 'end'>, <Token CLOSE_SQUARE_BRACKET - ']'>, <Token PIPE - '|'>, <Token OPEN_CURLY_BRAKET - '{'>, <Token mapping_key - 'firstName1:'>, <Token STRING - '"Hello1"'>, <Token COMMA - ','>, <Token mapping_key - '_last_name1:'>, <Token STRING - '"World1"'>, <Token COMMA - ','>, <Token mapping_key - 'int1:'>, <Token number - '1231'>, <Token COMMA - ','>, <Token mapping_key - 'float1:'>, <Token number - '34.561'>, <Token COMMA - ','>, <Token mapping_key - 'exp1:'>, <Token number - '1.234E+7'>, <Token COMMA - ','>, <Token mapping_key - 'negative1:'>, <Token number - '-1.235E+7'>, <Token COMMA - ','>, <Token mapping_key - 'money1:'>, <Token VARIAVBLE - '$bankBalance1'>, <Token COMMA - ','>, <Token CLOSE_CURLY_BRAKET - '}'>, <Token CLOSE_PARENTHESIS - ')'>]""",
    "COMPLETE_PROGRAM_2": """[<Token DEF - 'def'>, <Token Identifiers - 'addmul'>, <Token OPEN_PARENTHESIS - '('>, <Token Identifiers - 'a'>, <Token SEMI_COLON - ';'>, <Token Identifiers - 'b'>, <Token CLOSE_PARENTHESIS - ')'>, <Token OPEN_PARENTHESIS - '('>, <Token Identifiers - 'a'>, <Token ADDITION - '+'>, <Token Identifiers - 'b'>, <Token CLOSE_PARENTHESIS - ')'>, <Token MULTIPLICATION - '*'>, <Token OPEN_PARENTHESIS - '('>, <Token Identifiers - 'a'>, <Token SUBTRACTION - '-'>, <Token Identifiers - 'b'>, <Token CLOSE_PARENTHESIS - ')'>, <Token SEMI_COLON - ';'>, <Token OPEN_PARENTHESIS - '('>, <Token STRING - '"12"'>, <Token CLOSE_PARENTHESIS - ')'>, <Token AS - 'as'>, <Token VARIAVBLE - '$input'>, <Token PIPE - '|'>, <Token VARIAVBLE - '$input'>, <Token PIPE - '|'>, <Token Identifiers - 'addmul'>, <Token OPEN_PARENTHESIS - '('>, <Token number - '5'>, <Token SEMI_COLON - ';'>, <Token access_variable - '.value'>, <Token CLOSE_PARENTHESIS - ')'>, <Token PIPE - '|'>, <Token OPEN_CURLY_BRAKET - '{'>, <Token mapping_key - 'result:'>, <Token access_variable - '.,'>, <Token mapping_key - 'double:'>, <Token OPEN_PARENTHESIS - '('>, <Token access_variable - '. '>, <Token MULTIPLICATION - '*'>, <Token number - '2'>, <Token CLOSE_PARENTHESIS - ')'>, <Token CLOSE_CURLY_BRAKET - '}'>]""",
    "COMPLETE_PROGRAM_3": """[<Token IF - 'if'>, <Token access_variable - '.age'>, <Token GREATER_THAN_EQUAL - '>='>, <Token number - '18'>, <Token THEN - 'then'>, <Token STRING - '"adult"'>, <Token ELIL - 'elif'>, <Token access_variable - '.age'>, <Token GREATER_THAN_EQUAL - '>='>, <Token number - '13'>, <Token THEN - 'then'>, <Token STRING - '"teenager"'>, <Token ELSE - 'else'>, <Token STRING - '"child"'>, <Token END - 'end'>]""",
    "COMPLETE_PROGRAM_4": """[<Token access_variable - '.people'>, <Token OPEN_SQUARE_BRACKET - '['>, <Token CLOSE_SQUARE_BRACKET - ']'>, <Token PIPE - '|'>, <Token Identifiers - 'select'>, <Token OPEN_PARENTHESIS - '('>, <Token access_variable - '.active'>, <Token EQUALS - '=='>, <Token Identifiers - 'true'>, <Token CLOSE_PARENTHESIS - ')'>, <Token PIPE - '|'>, <Token OPEN_CURLY_BRAKET - '{'>, <Token Identifiers - 'name'>, <Token COMMA - ','>, <Token mapping_key - 'emails:'>, <Token OPEN_SQUARE_BRACKET - '['>, <Token access_variable - '.contacts'>, <Token OPEN_SQUARE_BRACKET - '['>, <Token CLOSE_SQUARE_BRACKET - ']'>, <Token QUESTION_MARK - '?'>, <Token access_variable - '.email'>, <Token DIVISION - '/'>, <Token DIVISION - '/'>, <Token STRING - '"unknown"'>, <Token CLOSE_SQUARE_BRACKET - ']'>, <Token CLOSE_CURLY_BRAKET - '}'>]""",
    "COMPLETE_PROGRAM_5": """[<Token DEF - 'def'>, <Token Identifiers - 'greet'>, <Token OPEN_PARENTHESIS - '('>, <Token Identifiers - 'name'>, <Token CLOSE_PARENTHESIS - ')'>, <Token STRING - '"Hello, name)! Today is now | strftime("'>, <Token MODULUS - '%'>, <Token Identifiers - 'A'>, <Token STRING - '"))."'>, <Token SEMI_COLON - ';'>, <Token Identifiers - 'greet'>, <Token OPEN_PARENTHESIS - '('>, <Token access_variable - '.username'>, <Token CLOSE_PARENTHESIS - ')'>]"""
}