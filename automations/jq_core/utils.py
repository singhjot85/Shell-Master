import re
import unicodedata

class StringNormalizer:
    """
    This normalizer can be used to normalize a string,
    It takes a string input, normalizes it spaces and newlines,
    It also preserves strings inside a string.
    """
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
    
    def _extract_string_mappings(self, s: str) -> dict:
        """
        Extract quoted strings and replace them with placeholders.
        Returns a mapping {placeholder: original_string}.
        """
        string_mapping = {}
        result = []
        is_string = False
        temp_str = []
        placeholder_count = 0

        for ch in s:
            if ch == '"':
                if is_string: # closing string
                    actual_str = ''.join(temp_str)
                    placeholder = f"__STR_{placeholder_count}__"
                    string_mapping[placeholder] = f'"{actual_str}"'
                    result.append(placeholder)
                    temp_str = []
                    placeholder_count += 1
                is_string = not is_string
            else:
                if is_string:
                    temp_str.append(ch)
                else:
                    result.append(ch)

        return ''.join(result), string_mapping

    def _restore_strings(self, s: str, mapping: dict) -> str:
        """Restore placeholders with original strings."""
        for placeholder, original in mapping.items():
            s = s.replace(placeholder, original)
        return s

    def normalize(
        self, 
        remove_spaces: bool = False,
        remove_controls: bool = False,
        prevent_nested: bool = True
    ) -> str:
        """
        Normalizes the string.
        Args:
            remove_spaces (bool): Entirely remove all the spaces.
            remove_controls (bool): Remove \n,\t and other control characters.
            prevent_nested (bool): Prevent the structure of strings nested inside input string.
        """
        s = self.program.strip()

        mapping = {}
        if prevent_nested:
            s, mapping = self._extract_string_mappings(s)

        s = self._collapse_whitespace(s)
        
        if remove_controls:
            s = self._remove_control_characters(s)
            s = self._remove_newline_tabline(s)

        if remove_spaces:
            s = self._remove_whitespaces(s)

        # Restore quoted/nested strings
        if prevent_nested and mapping:
            s = self._restore_strings(s, mapping)

        return s
