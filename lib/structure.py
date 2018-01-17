### Data structures
from enum import Enum
from constants import *
from logic import *

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

    def to_json(self):
        diffs = {}
        for date in self.diffs:
            diffs[datetime_to_shorttime(date)] = [diff.to_json() for diff in self.diffs[date]]
        dates = [datetime_to_shorttime(date) for date in self.dates]

        texts = {}
        for date in self.texts:
            texts[datetime_to_shorttime(date)] = self.texts[date]

        subsections = [s.to_json() for s in self.subsections]
        return {API.STRUCTURE_SECTION: self.section,
                API.STRUCTURE_REPRESENTATION: self.representation,
                API.STRUCTURE_NAME: self.name,
                API.STRUCTURE_DATES: dates,
                API.STRUCTURE_TEXTS: texts,
                API.STRUCTURE_DIFFS: diffs,
                API.STRUCTURE_SUBSECTIONS: subsections}

class Diff():
    def __init__(self, diff_type, position=None, add=None, remove=None, update=None):
        self.diff_type = diff_type
        self.position = position
        self.add = add
        self.remove = remove
        self.update = update

    def to_json(self):
        json = {API.DIFF_TYPE: self.diff_type}
        if self.position is not None:
            json[API.DIFF_POSITION] = self.position
        if self.add is not None:
            json[API.DIFF_ADD] = self.add
        if self.remove is not None:
            json[API.DIFF_REMOVE] = self.remove
        if self.update is not None:
            json[API.DIFF_UPDATE] = self.update.to_json()
        return json

