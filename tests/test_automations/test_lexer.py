""" Pytests to insure Lexer stays intact """
import logging
from automations.jq_core.lexer import Lexer
from tests.test_automations.dummy_data import TESTCASE_RESULTS_TYPE_1

LOGGER = logging.getLogger(__name__)

class TestLexer:
    def setup(self):
        LOGGER.info("---------- Testing Lexer ----------")
        
    def test_no_brackerts(self):
        LOGGER.info("TestCases Type: No Brackets")

        for x, (program, result) in enumerate(TESTCASE_RESULTS_TYPE_1.items(), start=0):
            LOGGER.info("Testcase no: %s, Program >>> %s", x+1, program)
            tokens = Lexer(program).tokenize()

            assert isinstance(tokens, list) == True
            assert len(tokens) == len(result)
            assert tokens == result

            
        