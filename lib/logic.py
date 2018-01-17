# Utility methods
import datetime

SHORTTIME_FORMAT = '%Y%m%d'

def shorttime_to_datetime(string):
    return datetime.datetime.strptime(string, SHORTTIME_FORMAT)

def datetime_to_shorttime(date):
    return date.strftime(SHORTTIME_FORMAT)

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
