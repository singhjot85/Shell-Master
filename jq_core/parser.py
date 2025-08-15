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

    def _remove_all_whitespace(self, s: str) -> str:
        """
        Remove all whitespace entirely.
        """
        return re.sub(r'\s+', '', s)

    def normalize(self, strip_edges: bool, collapse_spaces: bool = True) -> str:
        """
        Normalizes the string.

        Args:
            strip_edges: If True, trim leading/trailing whitespace after normalization.
            collapse_spaces: 
                If True, multiple spaces → single space.
                If False, all whitespace removed.
        """
        s = self.program
        s = self._remove_control_characters(s)

        if collapse_spaces:
            s = self._collapse_whitespace(s)
        else:
            s = self._remove_all_whitespace(s)
        
        if strip_edges and collapse_spaces:
            s = s.strip()

        return s

class BaseParser:
    """
    This parser would be used to parse jq programs, 
    so that they can be used by any other service.
    Args:
        program(str): JQ program to parse
    """
    def __init__(self, program: str):
        self.program = program

    def parse_sts(self):
        """
        A string to string parser, takes a string jq program as input,
        and parse it for other tools.
        """
        normalizer = StringNormalizer(self.program)
        return normalizer.normalize(collapse_spaces=False, strip_edges=True)