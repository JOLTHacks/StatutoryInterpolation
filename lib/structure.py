### Data structures
from enum import IntEnum
from constants import *
from logic import *

class DiffType(IntEnum):
    ADD = 0
    REMOVE = 1
    UPDATE = 2

class Structure():
    """A path to an arbitrary portion of the U.S. Code.
    Recursive data structure."""
    # May want to add text, diff for single-time Structure representation
    def __init__(self, name, section, order, dates=[], texts={}, diffs={}, subsections=[]):
        self.name = name
        self.section = section
        self.order = order
        self.dates = dates # Invariant: should be sorted
        self.texts = texts
        self.diffs = diffs
        self.subsections = subsections

    def get_text_at(self, date):
        subsections = [s.get_text_at(date) for s in self.subsections]
        structure = Structure(self.name, self.section, self.order,
                              subsections=subsections)
        if not self.has_text():
            return structure
        if date < self.dates[0]: # Did not exist at this date, may want to handle differently.
            return Structure(self.name, self.section, self.order)
        closest_date_index = 0
        while closest_date_index + 1 < len(self.dates) and self.dates[closest_date_index+1] < date:
            closest_date_index += 1
        closest_date = self.dates[closest_date_index]
        return Structure(self.name, self.section, self.order,
                         [closest_date], {closest_date: self.texts[closest_date]},
                         {closest_date: self.diffs[closest_date]}, subsections)

    def insert_date(self, date):
        if len(self.dates) == 0:
            self.dates.append(date)
            return 0
        cmp_ = 0
        ## Use binary search here eventually. But it's only 10 items so sustainable for now.
        while date > self.dates[cmp_]:
            cmp_ += 1
        if date != self.dates[cmp_]:
            self.dates.insert(cmp_, date)
            self.texts[date] = '' ## This could be a list
            self.diffs[date] = []
            return -cmp_
        return cmp_

    ## TODO(kxia): this probably needs to be add_structure_at and be linked to
    ##   loading structure, but I'm precoding structure for now.
    def add_text_at(self, path, date, text):
        if len(path) == 0:
            self.insert_date(date)
            self.texts[date] = text
        else:
            # Ensure path exists
            subsection = None
            for section in self.subsections:
                if section.order == path[0]:
                    subsection = section
                    break
            if not subsection:
                self.subsections.append(Structure('TEMP', 'TEMP', path[0]))
                subsection = self.subsections[-1]
            # Traverse path
            subsection.add_text_at(path[1:], date, text)

    def add_diff_at(self, path, date, diff):
        if len(path) == 0:
            self.insert_date(date)
            self.diffs[date].append(diff)
        else:
            # Path should always already exist
            subsection = None
            for section in self.subsections:
                if section.order == path[0]:
                    subsection = section
                    break
            # Traverse path
            subsection.add_diff_at(path[1:], date, diff)

    def has_children(self):
        return len(self.subsections) > 0

    def get_subsection_keys(self):
        return [subsection.order for subsection in self.subsections]

    def get_subsection(self, order):
        for subsection in self.subsections:
            if subsection.order == order:
                return subsection
        return None

    def has_subsection(self, order):
        return get_subsection is not None

    def has_text(self):
        return len(self.dates) > 0 and len(self.texts) > 0

    def short_str(self):
        return "%s %s" % (self.name, self.section)

    def to_json(self):
        diffs = {}
        for date in self.diffs:
            diffs[datetime_to_shorttime(date)] = [diff.to_json() for diff in self.diffs[date]]
        dates = [datetime_to_shorttime(date) for date in self.dates]

        texts = {}
        for date in self.texts:
            texts[datetime_to_shorttime(date)] = self.texts[date]

        subsections = [s.to_json() for s in self.subsections]
        json = {API.STRUCTURE_NAME: self.name,
                API.STRUCTURE_SECTION: self.section,
                API.STRUCTURE_ORDER: self.order}
        if len(dates) > 0:
            json[API.STRUCTURE_DATES] = dates
        if len(texts) > 0:
            json[API.STRUCTURE_TEXTS] = texts
        if len(diffs) > 0:
            json[API.STRUCTURE_DIFFS] = diffs
        if len(subsections) > 0:
            json[API.STRUCTURE_SUBSECTIONS] = subsections
        return json

    def __str__(self):
        return str(self.to_json())

class Diff():
    def __init__(self, diff_type, position=None, add=None, remove=None, update=None):
        self.diff_type = diff_type
        self.position = position
        self.add = add
        self.remove = remove
        self.update = update

    def to_json(self):
        json = {API.DIFF_TYPE: self.diff_type.value}
        if self.position is not None:
            json[API.DIFF_POSITION] = self.position
        if self.add is not None:
            json[API.DIFF_ADD] = self.add
        if self.remove is not None:
            json[API.DIFF_REMOVE] = self.remove
        if self.update is not None:
            ## TODO(kxia): update this once the link structure is tied down
            try:
                json[API.DIFF_UPDATE] = self.update.to_json()
            except AttributeError:
                json[API.DIFF_UPDATE] = self.update
        return json

    def __str__(self):
        return str(self.to_json())

