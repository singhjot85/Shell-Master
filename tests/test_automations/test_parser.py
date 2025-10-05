import logging
from automations.jq_core import Parser, Lexer, TokenType
from automations.jq_core.ast import *
from tests.test_automations.dummy_data import (
    create_token,
    TESTCASE_RESULTS_TYPE_1,
    TESTCASE_RESULTS_COMPLETE_PROGRAMS
)

LOGGER = logging.getLogger(__name__)

class TestParser:

    def setup(self):
        LOGGER.info("---------- Testing Parser ----------")

    def test_simple_case_parsing(self):
        p = r'12'
        tokens = Lexer(p).tokenize()
        ast = Parser(tokens).parse()
        assert tokens[0] == create_token(TokenType.NUMBER, 12)
        assert ast == NumberLiteral(float(p))

        p = '"Lol"'
        tokens = Lexer(p).tokenize()
        ast = Parser(tokens).parse()
        assert tokens[0] == create_token(TokenType.STRING, "Lol")
        assert ast == StringLiteral("Lol")

        p = r'null'
        tokens = Lexer(p).tokenize()
        ast = Parser(tokens).parse()
        assert tokens[0] == create_token(TokenType.NULL)
        assert ast == NullLiteral()

        p = '.'
        tokens = Lexer(p).tokenize()
        ast = Parser(tokens).parse()
        assert tokens[0] == create_token(TokenType.DOT)
        assert ast == Identity()