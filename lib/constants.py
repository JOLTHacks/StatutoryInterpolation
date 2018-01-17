## Server Values ##

class Server:
    HOST = '0.0.0.0'
    PORT = 5000

## API Values ##

class API:
    ## Outgoing keys
    GET_TITLES_KEY = 'titles'

    STRUCTURE_SECTION = 'section'
    STRUCTURE_REPRESENTATION = 'representation'
    STRUCTURE_NAME = 'name'
    STRUCTURE_DATES = 'dates'
    STRUCTURE_TEXTS = 'texts'
    STRUCTURE_DIFFS = 'diffs'
    STRUCTURE_SUBSECTIONS = 'subsections'

    DIFF_TYPE = 'type'
    DIFF_POSITION = 'position'
    DIFF_ADD = 'add'
    DIFF_REMOVE = 'remove'
    DIFF_UPDATE = 'update'

    ## Incoming keys
    TITLE_KEY = 'title'
