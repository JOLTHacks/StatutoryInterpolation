## Run-once server load methods.
from structure import Representation, DiffType, Diff, Structure
import datetime

def load_diffs():
    date_2011 = datetime.datetime(year=2011, month=1, day=1)
    date_2012 = datetime.datetime(year=2012, month=1, day=1)
    diff_2012 = [Diff(DiffType.ADD, position=4, add='u'),
                 Diff(DiffType.REMOVE, position=4, remove=1)]
    title_12_subsections = [Structure(1, Representation.ROMAN, 'Part'),
                            Structure(3, Representation.ROMAN, 'Part')]
    title_12_subsections[0].subsections = [Structure(1, Representation.UPPERCASE, 'Section'),
                                           Structure(2, Representation.UPPERCASE, 'Section')]
    title_12 = Structure(12, Representation.NUMERIC, 'Title',
                         dates=[date_2011, date_2012],
                         texts={date_2011: 'Hello', date_2012: 'Hellu'},
                         diffs={date_2011: [], date_2012: diff_2012},
                         subsections=title_12_subsections)
    return {12: title_12}

def print_structure(structure, depth=0):
    print ('\t' * depth) + structure.short_str()
    if not structure.has_children():
        return
    for s in structure.subsections:
        print_structure(s, depth=depth+1)
