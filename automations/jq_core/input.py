from abc import abstractmethod
from . import NEW_LINES, StringHandlerException

class BaseInputHandler:

    @abstractmethod
    def peek(self, offset: int = 0) -> str | None:
        """Return character at current+offset, without consuming it."""

    @abstractmethod
    def next(self) -> str | None:
        """Consume and return the next character."""

    @abstractmethod
    def eof(self) -> bool:
        """Return True if input is fully consumed."""

    @abstractmethod
    def position(self) -> tuple[int, int, int]:
        """Return (line, col, absolute_index)."""

    @abstractmethod
    def save(self) -> int:
        """Return a checkpoint index to allow rollback."""

    @abstractmethod
    def restore(self, checkpoint: int) -> None:
        """Restore input pointer to a previous checkpoint."""

    @abstractmethod
    def sync_handler(self):
        """Sync handler variables to the head, 
        if somehow it gets out of sync
        """

class CheckPoint:
    checkpoint_index: int = 0
    checkpoint_char:str = None
    checkpoint_line: int = 0
    checkpoint_col: int = 0

    def __init__(self, **kwarg):
        """
        Args:
            idx (int): Checkpoint index
            line (int): Checkpoint line
            col (int): Checkpoint column
            char (str): Checkpoint Char
        """
        self.checkpoint_index = kwarg.get("idx")        
        if not self.checkpoint_index:
            raise Exception("Checkpoint requires index to save")
        self.checkpoint_char = kwarg.get("char")
        self.checkpoint_line = kwarg.get("line")
        self.checkpoint_line = kwarg.get("col")

class StringInputHandler(BaseInputHandler):
    """Handler to iterate a string input source"""

    def __init__(self, text: str):
        self.text = text
        self.size = len(text)

        self.char = text[0] if self.text else None
        self.index = 0

        self.line = 0
        self.col = 0

    def peek(self) -> str:
        """Returns the next character does not move the pointer """
        if not self.eof():
            return self.text[self.index + 1]
        else:
            return None

    def next(self) -> str:
        """ moves to next character and returns it """
        if not self.eof():
            self.index += 1
            self.col += 1

            if not self.eof():
                self.char = self.text[self.index]
                 
                # Handler will never be on newline
                if self.char in NEW_LINES:
                    self.handle_newline()
                return self.char

        self.char = None
        return None

    def eof(self) -> bool:
        return self.index >= self.size

    def position(self):
        """Return (line, col, absolute_index)."""
        return self.line, self.col, self.index

    def save(self) -> CheckPoint:
        """Return a checkpoint index to allow rollback."""
        save_params = {
            "idx": self.index,
            "line": self.line,
            "col": self.col
        }
        return CheckPoint(**save_params)

    def restore(self, checkpoint: CheckPoint):
        """Restore input pointer to a previous checkpoint."""
        self.line = checkpoint.checkpoint_line
        self.col = checkpoint.checkpoint_col
        self.index = checkpoint.checkpoint_index
        self.char = self.text[self.index]

    def handle_newline(self):
        while (
            self.char in NEW_LINES
            and not self.eof()
        ):
            self.index += 1
            if not self.eof:
                self.char = self.text[self.index]

            self.line += 1
            self.col = 0

    def sync_handler(self):
        self.size = len(self.text)
        if self.index > self.size:
            raise StringHandlerException("Index out of program bounds")

        self.char = self.text[self.index]
        for idx, char in enumerate(self.text):
            if idx == self.index:
                break
            self.col += 1
            if char in NEW_LINES:
                self.line += 1
                self.col = 0

class BytesInputHandler(StringInputHandler):
    """Handler to iterate over a byte input
    To read directly from a network/file"""
    def __init__(self, text):
        """Simplest implementation is to re-use a string a handler
        Later on a fast handler can be devloped"""
        super().__init__(text)

class StreamInputHandler(BaseInputHandler):
    """Handler for a continous stream of file
    Needed in case of large files, for scalability
    Consume the programs in chunks"""
    pass