""" Pytests to insure Lexer stays intact """
import logging
from automations.jq_core.lexer import Lexer
from tests.test_automations.dummy_data import (
    TESTCASE_RESULTS_TYPE_1, 
    TESTCASE_RESULTS_COMPLETE_PROGRAMS
)

LOGGER = logging.getLogger(__name__)

class TestLexer:
    def setup(self):
        LOGGER.info("---------- Testing Lexer ----------")
        
    def test_no_brackerts(self):
        LOGGER.info("TestCases Type: No Brackets")

        for x, (program, result) in enumerate(TESTCASE_RESULTS_TYPE_1.items(), start=0):
            LOGGER.info("Testcase no: %s, \nProgram >>> %s", x+1, program)
            tokens = Lexer(program).tokenize()

            assert isinstance(tokens, list) == True
            assert len(tokens) == len(result)
            for i, _ in enumerate(result):
                LOGGER.info("Current Token number %s", i)
                LOGGER.info("Computed Token %s, Predefined Token %s", tokens[i], result[i])
                assert tokens[i].type == result[i].type
                assert tokens[i].value == result[i].value
    
    def test_complete_program(self):
        LOGGER.info("TestCases Type: COMPLETE PROGRAMS")

        for x, (program, result) in enumerate(TESTCASE_RESULTS_COMPLETE_PROGRAMS.items(), start=0):
            LOGGER.info("Testcase no: %s, Program >>> %s", x+1, program)
            tokens = Lexer(program).tokenize()

            assert isinstance(tokens, list) == True
            assert tokens.__str__() == result
    
    def test_line_col_positions(self):
        pass