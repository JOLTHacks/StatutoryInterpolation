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
        1: lambda x: num_to_roman(x),
        2: lambda x: num_to_roman(x, lowercase=True),
        3: lambda x: chr(x + ord('A') - 1),
        4: lambda x: chr(x + ord('a') - 1)
        }[r](n)

def num_to_roman(n, lowercase=False):
    '''Convert number to roman numerals. Does not handle 0.'''
    is_negative = False
    if n < 0:
        n *= -1
        is_negative = True
        
    values = [1000, 900, 500, 400, 100,90, 50, 40, 10, 9, 5, 4, 1]
    symbols = {1000:'M', 900:'CM', 500: 'D', 400:'CD', 100:'C', 90:'XC',
               50:'L', 40:'XL', 10:'X', 9:'IX', 5:'V', 4:'IV', 1:'I'}
    string = ''
    for v in values:
        if n == 0:
            break
        x, y = divmod(n, v)
        string += symbols[v] * x
        n -= v * x

    return ('-' if is_negative else '') + (string.lower() if lowercase else string)

class DiffType(Enum):
    ADD = 0
    REMOVE = 1
    UPDATE = 2

class Structure():
    """A path to an arbitrary portion of the U.S. Code.
    Recursive data structure."""
    # May want to add text, diff for single-time Structure representation
    def __init__(self, section, representation, name, dates=[], texts={}, diffs={}, subsections=[]):
        self.section = section
        self.representation = representation
        self.name = name
        self.dates = dates # Invariant: should be sorted
        self.texts = texts
        self.diffs = diffs
        self.subsections = subsections

    def get_text_at(self, date):
        if date < self.dates[0]: # Did not exist at this date, may want to handle differently.
            return Structure(self.section, self.representation, self.name)
        closest_date_index = 0
        while closest_date_index + 1 < len(self.dates) and self.dates[closest_date_index+1] < date:
            closest_date_index += 1
        closest_date = self.dates[closest_date_index]
        subsections = [s.getTextAt(date) for s in self.subsections]
        return Structure(self.section, self.representation, self.name,
                         [closest_date], {closest_date: self.texts[closest_date]},
                         {closest_date: self.diffs[closest_date]}, subsections)

    def has_children(self):
        return len(self.subsections) > 0

    def short_str(self):
        return "%s %s" % (self.name, num_to_representation(self.section, self.representation))

class Diff():
    def __init__(self, diff_type, position=0, add='', remove=0, update=None):
        self.diff_type = diff_type
        self.position = position
        self.add = add
        self.remove = remove
        self.update = update

