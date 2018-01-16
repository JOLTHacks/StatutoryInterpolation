### Data structures
from enum import Enum

class Representation(Enum):
    NUMERIC = 0
    ROMAN = 1
    SMALL_ROMAN = 2
    UPPERCASE = 3
    LOWERCASE = 4

class DiffType(Enum):
    ADD = 0
    REMOVE = 1
    UPDATE = 2

class Structure():
    """A path to an arbitrary portion of the U.S. Code.
    Recursive data structure."""
    def __init__(self, section, representation, text=None, diffs=[], subsections=[]):
        self.section = section
        self.representation = representation
        self.text = text
        self.diffs = diffs
        self.subsections = subsections

    def has_children():
        return len(self.subsections) > 0

