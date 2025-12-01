"""Pytests to insure Lexer stays intact"""

import logging

from automations.jq_core.lexer import Lexer
from tests.test_automations.dummy_data import (
    COMPLETE_PROGRAMS,
    COMPLETE_PROGRAMS_RESULTS,
    INPUT_TYPE_1,
    RESULT_TYPE_1,
)

LOGGER = logging.getLogger(__name__)


class TestLexer:
    def setup(self):
        LOGGER.info("---------- Testing Lexer ----------")

    def test_simple_cases(self):
        LOGGER.info("TestCases Type: Simple Short Program")

        for test_case, program in INPUT_TYPE_1.items():
            expected_result = RESULT_TYPE_1[test_case]

            LOGGER.info("Testcase no: %s, \nProgram >>> %s", test_case, program)
            tokens = Lexer(program).tokenize()

            LOGGER.info("Expected >>> %s, \n Recieved >>> %s", expected_result, tokens)
            assert isinstance(tokens, list)
            # assert len(tokens) == len(expected_result)
            assert tokens.__str__() == expected_result

    def test_simple_large_programs(self):
        LOGGER.info("TestCases Type: Simple Large Program")

        for test_case, program in COMPLETE_PROGRAMS.items():
            expected_result = COMPLETE_PROGRAMS_RESULTS[test_case]

            LOGGER.info("Testcase no: %s, \nProgram >>> %s", test_case, program)
            tokens = Lexer(program).tokenize()

            LOGGER.info("Expected >>> %s, \n Recieved >>> %s", expected_result, tokens)
            assert isinstance(tokens, list)
            # assert len(tokens) == len(expected_result)
            assert tokens.__str__() == expected_result

    def test_line_col_positions(self):
        pass
