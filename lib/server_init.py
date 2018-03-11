## Run-once server load methods.
from constants import *
from structure import DiffType, Diff, Structure
import datetime, logic

class LoadingDiff():
    """An intermediary diff used only when loading from files."""
    def __init__(self, path, date, diff):
        self.path = path
        self.date = date
        self.diff = diff

    def __str__(self):
        return '%s @ %s - %s' % (self.path, str(self.date), str(self.diff))

def construct_loading_diff(s):
    parts = s.split(',')
    path = parts[0].split(BACKEND.US_CODE_PATH_DELIMITER)
    date = logic.shorttime_to_datetime(parts[1])
    diff_type = DiffType(int(parts[2]))
    position = int(parts[3])
    add = parts[4]
    remove = int(parts[5])
    link = parts[6].split(BACKEND.US_CODE_PATH_DELIMITER)
    return LoadingDiff(path, date, Diff(diff_type, position, add, remove, link))

def read_diffs(src):
    file_ = open(src, 'r')
    return [construct_loading_diff(line) for line in file_.readlines()]

def load_diffs(src):
    ## Assume there is some existing code structure
    # structure = Structure(
    loading_diffs = read_diffs(src)
    for diff in loading_diffs:
        print str(diff)
    date_2011 = datetime.datetime(year=2011, month=1, day=1)
    date_2012 = datetime.datetime(year=2012, month=1, day=1)
    diff_2012 = [Diff(DiffType.ADD, position=4, add='u'),
                 Diff(DiffType.REMOVE, position=4, remove=1)]
    title_12_subsections = [Structure('Part', 'I', 0),
                            Structure('Part', 'III', 2)]
    title_12_subsections[0].subsections = [Structure('Section', 'A', 0),
                                           Structure('Section', 'B', 1)]
    title_12 = Structure('Title', '12', 11,
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
