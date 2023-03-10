# Imports
from z3 import *
import numpy as np
from collections import deque

#==================================
# Constants
l_grid_size = 12
s_grid_size = 7
starting_point = [0,5]

#==================================
# Variables
def findNNs(cells, max_n):
    grid_number_c = []
    for n in range(1, 1 + max_n):
        s = Sum([If(c == n, 1, 0) for c in cells]) == n
        grid_number_c.append(s)
    return grid_number_c

def is_fully_connected(matrix):
    rows, cols = len(matrix), len(matrix[0])
    visited = [[False] * cols for _ in range(rows)]
    q = deque()
    connected_components = 0

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1 and not visited[i][j]:
                # Start a new connected component
                connected_components += 1
                q.append((i, j))
                visited[i][j] = True
                while q:
                    x, y = q.popleft()
                    # Visit all the neighbors of the current cell
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if (
                            0 <= nx < rows
                            and 0 <= ny < cols
                            and matrix[nx][ny] == 1
                            and not visited[nx][ny]
                        ):
                            q.append((nx, ny))
                            visited[nx][ny] = True

    # Check if there is only one connected component
    return connected_components == 1


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


# for finding 1 1s to 7 7s
grid_number_c = []
for i0 in starting_point:
    for j0 in starting_point:
        cells = [X[i][j] for i in range(i0,i0+s_grid_size) for j in range(j0,j0+s_grid_size)]
        grid_number_c+=findNNs(cells, s_grid_size)

# for checking 2x2 subgrid has at least an empty space
subgrid_22_empty = []
subgrid_2_size = 2
for i0 in range(l_grid_size-1):
    for j0 in range(l_grid_size-1):
        cells = [X[i][j] for i in range(i0,i0+subgrid_2_size) for j in range(j0,j0+subgrid_2_size)]
        s = Sum([If(c == 0, 1, 0) for c in cells]) >= 1
        subgrid_22_empty.append(s)






tfs_c = [ If(tfs_array[i][j] == 0, 
                  True, 
                  X[i][j] == tfs_array[i][j]) 
               for i in range(12) for j in range(12) ]

final_c = cell_c + grid_number_c + tfs_c + subgrid_22_empty

s = Solver()
s.add(final_c)
while True:
    if s.check() == sat:
        m = s.model()
        r = [[m.evaluate(X[i][j]) for j in range(12)] for i in range(12)]
        print_matrix(r)
        if is_fully_connected(r):
            print_matrix(r)    
            break
        else:
            print("rerun")
            new_c = Not(And([X[i][j] == r[i][j] for j in range(12) for i in range(12)]))
            s.add(new_c)
    else:
        print("failed to solve")
        break
