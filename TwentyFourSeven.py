# Imports 
from z3 import *

# Twenty-Four-Seven Array
tfs_array = (
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 0, 0, 0, 0, 0, 6, 5, 0),
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
row_constr_left = [5,7,7,33,29,2,40,28,0,0,36,0]
row_constr_right=[4,0,0,1,0,0,0,0,0,0,0,7]

column_constr_top=[6,36,30,34,27,3,40,27,0,0,7,0]
column_constr_bottom=[6,0,0,4,0,0,0,0,0,0,0,5]

#Grid printer
def print_grid(g):
    lines = []
    for row in g:
        lines.append(' '.join(str(x) for x in row))
    print('\n'.join(lines))


s = Solver()

X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(12)] for i in range(12)]

def four_in_each_row(grid,c):
    # print_grid(grid)
    for i in range(7):
        c.add(Sum([If(grid[i][j] != 0,1,0) for j in range(7) ])==4)
    for j in range(7):
        c.add(Sum([If(grid[i][j] != 0,1,0) for i in range(7) ])==4)


def sum_of_rows(grid, c):
    # print_grid(grid)
    for i in range(7):
        c.add(Sum([If(grid[i][j] != 0,grid[i][j],0) for j in range(7) ])==20)
    for j in range(7):
        c.add(Sum([If(grid[i][j] != 0,grid[i][j],0) for i in range(7) ])==20)



constrs = None
sum_of_rows([row[:7] for row in X[:7]], constrs)