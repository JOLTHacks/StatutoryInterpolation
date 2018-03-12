## Run-once server load methods.
from constants import *
from structure import DiffType, Diff, Structure
import datetime, logic

def load_us_code(src):
    ## Invariant: for the meta-structure, order = title #.
    file_ = open(src, 'r')
    file_.close()
    mar1 = datetime.date(2018, 3, 1)
    structure = Structure('Title', '12', 12,
                          subsections=[Structure('Section', '2', 2,
                                                 dates=[mar1],
                                                 texts={mar1:''},
                                                 diffs={mar1:[]})])
    structure = Structure('US Code', '0', 0, subsections=[structure])
    return structure

class LoadingDiff():
    """An intermediary diff used only when loading from files."""
    def __init__(self, path, date, diff):
        self.path = path
        self.date = date
        self.diff = diff

    def to_json(self):
        return self.diff.to_json()

    def __str__(self):
        return '%s @ %s - %s' % (self.path, str(self.date), str(self.diff))

def construct_loading_diff(s):
    parts = s.split(',')
    path = [int(part) for part in parts[0].split(BACKEND.US_CODE_PATH_DELIMITER)]
    date = logic.shorttime_to_datetime(parts[1]).date()
    diff_type = DiffType(int(parts[2]))
    position = int(parts[3])
    add = parts[4]
    remove = int(parts[5])
    link = [int(part) for part in parts[6].split(BACKEND.US_CODE_PATH_DELIMITER)]
    return LoadingDiff(path, date, Diff(diff_type, position, add, remove, link))

def read_diffs(src):
    file_ = open(src, 'r')
    return [construct_loading_diff(line) for line in file_.readlines()]
    file_.close()

def load_diffs(src, structure):
    loading_diffs = read_diffs(src)
    for diff in loading_diffs:
        # Index into a larger map / meta-structure
        structure.add_diff_at(diff.path, diff.date, diff.diff)
    return structure

def print_structure(structure, depth=0):
    print ('\t' * depth) + structure.short_str()
    if not structure.has_children():
        return
    for s in structure.subsections:
        print_structure(s, depth=depth+1)
