from structure import Representation, DiffType, Structure

## Run-once server load methods.

def load_diffs():
    title_12 = Structure(12, Representation.NUMERIC, 'Title')
    title_12.subsections = [Structure(1, Representation.ROMAN, 'Part'),
                            Structure(3, Representation.ROMAN, 'Part')]
    title_12.subsections[0].subsections = [\
        Structure(1, Representation.UPPERCASE, 'Section'),
        Structure(2, Representation.UPPERCASE, 'Section')]
    return {12: title_12}

def print_structure(structure, depth=0):
    print ("\t" * depth) + structure.short_str()
    if not structure.has_children():
        return
    for s in structure.subsections:
        print_structure(s, depth=depth+1)

## Utility methods

SHORTTIME_FORMAT = '%Y%m%d'

def shorttime_to_datetime(string):
    return datetime.datetime.strptime(string, SHORTTIME_FORMAT)

def datettime_to_shorttime(date):
    return date.strftime(SHORTTIME_FORMAT)
