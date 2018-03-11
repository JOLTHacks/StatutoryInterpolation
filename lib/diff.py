# StatutoryInterpolation
# Diff.py
from HTMLParser import HTMLParser
from collections import OrderedDict
import string


class USCParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.start = 0
        self.dict = OrderedDict()
        self.path = ''
        self.date = ''

    def handle_data(self, data):
        for dstr in data.split():
            if self.start:
                self.dict[self.path].append(dstr)

    def handle_comment(self, data):
        if 'itempath' in data:
            self.path = data.split(' itempath:')[1].rstrip()
            self.start = 1
            if self.path not in self.dict:
                self.dict[self.path] = []
        if 'currentthrough' in data:
            self.date = data.split('currentthrough:')[1][:8]

    def get_dict(self):
        return self.dict


class Diff:
    def __init__(self, path='', date='', type='', pos=0, add='', remove=''):
        self.path = path
        self.date = date
        self.type = type
        self.pos = pos
        self.add = add
        self.remove = remove
        # self.link = link

    def getcsv(self):
        return ','.join((self.path, self.date, str(self.type), str(self.pos), self.add, self.remove))


class DivisionDiff:
    def __init__(self, d1, d2, key):
        self.diffs = []
        self.subdivs = []

        l1 = []
        l2 = []
        sd1 = {}
        sd2 = {}
        q1 = []
        q2 = []

        # Matters which version goes first
        for k in d1:
            if k.endswith(key):
                for item in d1[k]:
                    l1.append((k, item))
            elif key + '/' in k and '/' not in k.split(key + '/')[1]:
                q1.append(k)
                sd1[k] = list(d1[k])
            elif key + '/' in k:
                sd1[k] = list(d1[k])
        for k in d2:
            if k.endswith(key):
                for item in d2[k]:
                    l2.append((k, item))
            elif key + '/' in k and '/' not in k.split(key + '/')[1]:
                q2.append(k)
                sd2[k] = list(d2[k])
            elif key + '/' in k:
                sd2[k] = list(d2[k])

        self.diffs = diff(l1, l2)

        for k in q2:
            self.subdivs.append(DivisionDiff(sd1, sd2, k))

    def totaldiff(self):
        ld = list(self.diffs)
        for div in self.subdivs:
            ld.extend(div.totaldiff())
        return ld


def diff(s1, s2):
    """Apply the Myers algorithm to generate a diff chart for 2 strings or 2 lists of words."""
    """The lists are expected to be tuples of the form (path to the word in the statute, word)"""
    # TODO: Implement Copy Functionality to Supplement Insertions and Deletions.
    # Initialize MAX and V as laid out in Figure 2 of the Myers Paper
    # Also initialize 2D array for tracking the optimal path to each node
    n = len(s1)
    m = len(s2)
    maxEdit = n + m
    if maxEdit == 0:
        return []
    V = []
    # path = [[[] for y in range(m+1)] for x in range(n+1)]
    for i in range(-maxEdit, maxEdit+1):
        V.append(-1)
    V[maxEdit+1] = 0
    trace = []
    done = 0

    for D in range(0, maxEdit+1):
        if done == 1:
            break

        trace.append(list(V))

        for k in range(-D, D+1, 2):
            if k == -D or (k != D and V[k-1+maxEdit] < V[k+1+maxEdit]):
                x = V[k+1+maxEdit]
                y = x - k
                # Add an insertion to the path to the given node
                # Insertion Format: INS (word) (index of gap into which word must be inserted, starting from 0)
                # if D != 0 and y - 1 < m:
                #     path[x][y] = list(path[x][y-1])
                #     path[x][y].append(Diff(s2[y-1][0], '', 'INS', x, s2[y-1][1], '').getcsv())
            else:
                x = V[k-1+maxEdit] + 1
                y = x - k
                # Add a deletion to the path to the given node
                # Deletion Format: DEL (word) (index of word to be deleted, starting from 1)
                # if D != 0 and x - 1 < n:
                #     path[x][y] = list(path[x-1][y])
                #     path[x][y].append(Diff(s1[x-1][0], '', 'DEL', x, '', s1[x-1][1]).getcsv())
            while x < n and y < m:
                if s1[x] == s2[y]:
                    x += 1
                    y += 1
                    # path[x][y] = list(path[x-1][y-1])
                else:
                    break
            V[k+maxEdit] = x
            if x >= n and y >= m:
                # print D
                done = 1
                break

    x = n
    y = m
    backward = []

    for v in reversed(trace):
        k = x - y
        if k == -D or (k != D and v[k-1+maxEdit] < v[k+1+maxEdit]):
            pk = k + 1
        else:
            pk = k - 1
        px = v[pk+maxEdit]
        py = px - pk

        while x > px and y > py:
            x = x - 1
            y = y - 1

        if x > px >= 0:
            backward.append(Diff(s1[px][0], '', '-', px, '', s1[px][1]).getcsv())
            x = x - 1
        elif y > py >= 0:
            backward.append(Diff(s2[py][0], '', '+', py, s2[py][1], '').getcsv())
            y = y - 1

        x = px
        y = py

    path = list(reversed(backward))
    return path


def parse(fname):
    """Parse an HTML file for a title of the US Code into a dictionary of lists of words organized by path."""
    # TODO: Handle Special Characters
    # TODO: Separate punctuation and preserve structure
    readfile = open(fname, 'r')
    parser = USCParser()
    # parser.feed(parser.unescape(readfile.read()))
    parser.feed(readfile.read())
    for key in parser.get_dict():
        print key
    return parser.get_dict()


def divisiondiff(fname1, fname2, div, num):
    """Given HTML docs for two US Code Versions, get a diff for the piece given by the division and the number."""
    # TODO: How Do We Handle Changes to Section Number Between Versions?
    # TODO: Handle Section Ranges (# To #) (Also, getting too much text, all sections in range)
    d1 = parse(fname1)
    d2 = parse(fname2)

    l1 = []
    l2 = []

    if div == 'section':
        for key in d1:
            if key.endswith('Sec. ' + str(num)):
                # l1 = list(d1[key])
                for item in d1[key]:
                    l1.append((key, item))
            elif len(key.split('Sec. ' + str(num))) > 1:
                if key.split('Sec. ' + str(num))[1] in string.letters:
                    for item in d1[key]:
                        l1.append((key, item))
            elif 'Secs. ' in key:
                if (' ' + str(num) + ' ') in key or (' ' + str(num) + ',') in key or key.endswith(' ' + str(num)):
                    # l1 = list(d1[key])
                    for item in d1[key]:
                        l1.append((key, item))
                elif ' to ' in key:
                    if int(key.split('to')[0].split()[-1]) <= num <= int(key.split('to')[1].rstrip().lstrip()):
                        for item in d1[key]:
                            l1.append((key, item))
        for key in d2:
            if key.endswith('Sec. ' + str(num)):
                # l2 = list(d2[key])
                for item in d2[key]:
                    l2.append((key, item))
            elif len(key.split('Sec. ' + str(num))) > 1:
                if key.split('Sec. ' + str(num))[1] in string.letters:
                    for item in d2[key]:
                        l2.append((key, item))
            elif 'Secs. ' in key:
                if (' ' + str(num) + ' ') in key or (' ' + str(num) + ',') in key or key.endswith(' ' + str(num)):
                    # l2 = list(d2[key])
                    for item in d2[key]:
                        l2.append((key, item))
                elif ' to ' in key:
                    if int(key.split('to')[0].split()[-1]) <= num <= int(key.split('to')[1].rstrip().lstrip()):
                        for item in d2[key]:
                            l2.append((key, item))
    # The remaining logic assumes a structure akin to Title 18 (Title > Part > Chapter > Section)
    elif div == 'chapter':
        for key in d1:
            if ('CHAPTER ' + str(num) + '/') in key or key.endswith('Chapter ' + str(num)):
                # l1.extend(d1[key])
                for item in d1[key]:
                    l1.append((key, item))
            elif len(key.split('CHAPTER ' + str(num))) > 1:
                if key.split('CHAPTER ' + str(num))[1] in string.letters:
                    for item in d1[key]:
                        l1.append((key, item))
                elif len(key.split('CHAPTER ' + str(num))[1]) > 1:
                    if key.split('CHAPTER ' + str(num))[1][0] in string.letters:
                        for item in d1[key]:
                            l1.append((key, item))
        for key in d2:
            if ('CHAPTER ' + str(num) + '/') in key or key.endswith('Chapter ' + str(num)):
                # l2.extend(d2[key])
                for item in d2[key]:
                    l2.append((key, item))
            elif len(key.split('CHAPTER ' + str(num))) > 1:
                if key.split('CHAPTER ' + str(num))[1] in string.letters:
                    for item in d2[key]:
                        l2.append((key, item))
                elif len(key.split('CHAPTER ' + str(num))[1]) > 1:
                    if key.split('CHAPTER ' + str(num))[1][0] in string.letters:
                        for item in d2[key]:
                            l2.append((key, item))
    elif div == 'part':
        for key in d1:
            if ('PART ' + num + '/') in key or key.endswith('PART ' + str(num)):
                # l1.extend(d1[key])
                for item in d1[key]:
                    l1.append((key, item))
        for key in d2:
            if ('PART ' + num + '/') in key or key.endswith('PART ' + str(num)):
                # l2.extend(d2[key])
                for item in d2[key]:
                    l2.append((key, item))

    return diff(l1, l2)


def docdiff(fname1, fname2):
    """Given HTML docs for 2 US Code versions, generate the diff of the 2 versions."""
    d1 = parse(fname1)
    d2 = parse(fname2)

    mydiff = DivisionDiff(d1, d2, '/180/PART III')
    print(str(len(mydiff.totaldiff())))
    return mydiff.totaldiff()
