from z3 import *

X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(3)] for i in range(3)]

print(X)

cell_c = [And(0 <= X[i][j], X[i][j] <= 3) for i in range(3) for j in range(3)]


# checker for 1 1s, 2 2s
cells = [X[i][j] for i in range(3) for j in range(3)]

starting_point = [0,1]

def findNNs(cells, max_n):
    grid_number_c = []
    for n in range(1, 1 + max_n):
        s = Sum([If(c == n, 1, 0) for c in cells]) == n
        grid_number_c.append(s)
    return grid_number_c


s_grid_size = 2
grid_number_c = []
for i0 in starting_point:
    for j0 in starting_point:
        cells = [X[i][j] for i in range(i0,i0+s_grid_size) for j in range(j0,j0+s_grid_size)]
        
        print(cells)
        grid_number_c+=findNNs(cells, 2)

print(grid_number_c)

final_c = cell_c + grid_number_c
print(final_c)
s = Solver()
s.add(final_c)
if s.check() == sat:
    m = s.model()
    r = [[m.evaluate(X[i][j]) for j in range(3)] for i in range(3)]
    print_matrix(r)
else:
    print("failed to solve")
