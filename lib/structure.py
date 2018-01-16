### Data structures
from enum import Enum

class Representation(Enum):
    NUMERIC = 0
    ROMAN = 1
    SMALL_ROMAN = 2
    UPPERCASE = 3
    LOWERCASE = 4

def num_to_representation(n, r):
    return {
        0: lambda x: x,
        1: lambda x: x, ## TODO
        2: lambda x: x, ## TODO
        3: lambda x: chr(x + ord('A') - 1),
        4: lambda x: chr(x + ord('a') - 1)
        }[r](n)

class DiffType(Enum):
    ADD = 0
    REMOVE = 1
    UPDATE = 2

class Structure():
    """A path to an arbitrary portion of the U.S. Code.
    Recursive data structure."""
    def __init__(self, section, representation, name, text=None, diffs=[], subsections=[]):
        self.section = section
        self.representation = representation
        self.name = name
        self.text = text
        self.diffs = diffs
        self.subsections = subsections

    def has_children(self):
        return len(self.subsections) > 0

    def short_str(self):
        return "%s %s" % (self.name, num_to_representation(self.section, self.representation))

