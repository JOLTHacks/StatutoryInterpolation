## Server Values ##

class Server:
    HOST = '0.0.0.0'
    PORT = 5000

## API Values ##

class API:
    STRUCTURE_NAME = 'name'
    STRUCTURE_SECTION = 'section'
    STRUCTURE_ORDER = 'order'
    STRUCTURE_DATES = 'dates'
    STRUCTURE_TEXTS = 'texts'
    STRUCTURE_DIFFS = 'diffs'
    STRUCTURE_SUBSECTIONS = 'subsections'

    DIFF_TYPE = 'type'
    DIFF_POSITION = 'position'
    DIFF_ADD = 'add'
    DIFF_REMOVE = 'remove'
    DIFF_UPDATE = 'update'

    class KEYS:
        ## Outgoing
        GET_TITLES = 'titles'

        ## Incoming
        TITLE = 'title'

        #### getDiffs()
        STRUCTURE = 'structure'
        BEFORE = 'before'
        AFTER = 'after'
        DIFF_BEFORE = 'diffBefore'

class BACKEND:
    ## TODO(bgunning): replace this with whatever delimiter makes sense.
    ##   I've intentionally set it to ',' so it has to be changed later.
    DIFF_SOURCE = 'data/diffs.csv'
    US_CODE_PATH_DELIMITER = '.'
