from z3 import *

s = Solver()
test_array = ((1, 0, 0), (0, 0, 0), (0, 0, 1))
X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(3)] for i in range(3)]
B = [[Bool("b_%s_%s" % (i + 1, j + 1)) for j in range(3)] for i in range(3)]
Found = Bool("found")
tfs_c = [
    If(test_array[i][j] == 0, True, X[i][j] == test_array[i][j])
    for i in range(3)
    for j in range(3)
]

cell_c = [And(0 <= X[i][j], X[i][j] <= 1) for i in range(3) for j in range(3)]

def findNeighbours(X, i, j):
    nbs = []
    max = len(X)
    if i>0:
        nbs.append(X[i-1][j])
    if j>0:
        nbs.append(X[i][j-1])
    if i<max-1:
        nbs.append(X[i+1][j])
    if j<max-1:
        nbs.append(X[i][j+1])
    return nbs

for i in range(3):
    for j in range(3):
        Implies(X[i][j]!=0, findNeighbours(X,i,j))





s.add(tfs_c+cell_c)
if s.check() == sat:
    m = s.model()
    r = [[m.evaluate(X[i][j]) for j in range(3)] for i in range(3)]
    print_matrix(r)
else:
    print("failed to solve")
