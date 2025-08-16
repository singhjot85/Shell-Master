import re
import unicodedata

class StringNormalizer:
    def __init__(self, text: str):
        self.program = text

    def _remove_control_characters(self, s: str) -> str:
        """
        Removes all Unicode control characters.
        Category 'C' in Unicode includes:
        - ASCII control chars (0-31, 127)
        - Format chars (like zero-width space)
        - Line/paragraph separators
        """
        return ''.join(ch for ch in s if unicodedata.category(ch)[0] != 'C')

    def _collapse_whitespace(self, s: str) -> str:
        """
        Collapse all whitespace (including tabs, newlines, NBSP) into a single space.
        """
        return re.sub(r'\s+', ' ', s)

    def _remove_newline_tabline(self, s: str):
        return re.sub(r'\n+', '', re.sub(r'\t+', '', s))

    def _remove_whitespaces(self, s: str):
        """
        Remove all whitespace entirely.
        """
        return re.sub(r'\s+', '', s)

    def normalize(
        self, 
        remove_spaces: bool = False,
        remove_controls: bool = False
    ) -> str:
        """
        Normalizes the string.

        Args:
            remove_spaces (bool): Entirely remove all the spaces.
            remove_controls (bool): Remove \n,\t and other control characters.
        """
        s = self.program 
        s = s.strip()
        s = self._collapse_whitespace(s)
        
        if remove_controls:
            s = self._remove_control_characters(s)
            s = self._remove_newline_tabline(s)

        if remove_spaces:
            s = self._remove_whitespaces(s)

        return s

class BaseParser:
    """
    This parser would be used to parse jq programs, 
    so that they can be used by any other service.
    Args:
        program(str): JQ program to parse
    """
    def __init__(self):
        self.program = ''

    def parse_sts(self, program: str):
        """
        A string to string parser, takes a string jq program as input,
        and parse it for other tools.
        """
        self.program = program
        normalizer = StringNormalizer(self.program)
        if normalizer:
            self.program = normalizer.normalize(True,True)
        return self.program