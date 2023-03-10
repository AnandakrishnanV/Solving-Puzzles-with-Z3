# Imports
from z3 import *
import numpy as np



#==================================
def findNNs(cells, max_n):
    grid_number_c = []
    for n in range(1, 1 + max_n):
        s = Sum([If(c == n, 1, 0) for c in cells]) == n
        grid_number_c.append(s)
    return grid_number_c



#==================================
# Twenty-Four-Seven Array
tfs_array = (
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 0, 0, 0, 0, 0, 6, 5, 0),
    (0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 6, 0),
    (0, 4, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0),
    (0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 7),
    (0, 0, 6, 0, 0, 0, 0, 0, 3, 7, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 7, 0, 5, 0, 0, 0, 0, 0, 0),
    (0, 5, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0),
    (0, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0),
)

# Blue constraints
row_constr_left = [5, 7, 7, 33, 29, 2, 40, 28, 0, 0, 36, 0]
row_constr_right = [4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 7]

column_constr_top = [6, 36, 30, 34, 27, 3, 40, 27, 0, 0, 7, 0]
column_constr_bottom = [6, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 5]


s = Solver()

X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(12)] for i in range(12)]

# to ensure each cell is in 0..7
cell_c = [And(0 <= X[i][j], X[i][j] <= 7) for i in range(12) for j in range(12)]

starting_point = [0,5]
s_grid_size = 7

# for finding 1 1s to 7 7s
grid_number_c = []
for i0 in starting_point:
    for j0 in starting_point:
        cells = [X[i][j] for i in range(i0,i0+s_grid_size) for j in range(j0,j0+s_grid_size)]
        grid_number_c+=findNNs(cells, 7)

tfs_c = [ If(tfs_array[i][j] == 0, 
                  True, 
                  X[i][j] == tfs_array[i][j]) 
               for i in range(12) for j in range(12) ]

final_c = cell_c + grid_number_c + tfs_c

s = Solver()
s.add(final_c)
if s.check() == sat:
    m = s.model()
    r = [[m.evaluate(X[i][j]) for j in range(12)] for i in range(12)]
    print_matrix(r)
else:
    print("failed to solve")
