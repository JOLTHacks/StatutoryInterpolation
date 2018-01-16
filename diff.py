# StatutoryInterpolation
# Diff.py


def diff(s1, s2):
    """Apply the Myers algorithm to generate a diff chart for 2 strings or 2 lists of words."""

    # Initialize MAX and V as laid out in Figure 2 of the Myers Paper
    # Also initialize 2D array for tracking the optimal path to each node
    n = len(s1)
    m = len(s2)
    maxEdit = n + m
    V = []
    path = [[[] for y in range(m+1)] for x in range(n+1)]
    for i in range(-maxEdit, maxEdit+1):
        V.append(-1)
    V[maxEdit+1] = 0

    for D in range(0, maxEdit+1):
        for k in range(-D, D+1, 2):
            if k == -D or (k != D and V[k-1+maxEdit] < V[k+1+maxEdit]):
                x = V[k+1+maxEdit]
                y = x - k
                # Add an insertion to the path to the given node
                # Insertion Format: INS (word) (index of gap into which word must be inserted, starting from 0)
                if D != 0 and y - 1 < m:
                    path[x][y] = list(path[x][y-1])
                    path[x][y].append('INS ' + s2[y-1] + ' ' + str(x))
            else:
                x = V[k-1+maxEdit] + 1
                y = x - k
                # Add a deletion to the path to the given node
                # Deletion Format: DEL (word) (index of word to be deleted, starting from 1)
                if D != 0 and x - 1 < n:
                    path[x][y] = list(path[x-1][y])
                    path[x][y].append('DEL ' + s1[x-1] + ' ' + str(x))
            while x < n and y < m:
                if s1[x] == s2[y]:
                    x += 1
                    y += 1
                    path[x][y] = list(path[x-1][y-1])
                else:
                    break
            V[k+maxEdit] = x
            if x >= n and y >= m:
                print D
                return path[n][m]
