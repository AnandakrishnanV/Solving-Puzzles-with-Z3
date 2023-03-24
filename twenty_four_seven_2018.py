#Jane Street 2018
# The grid is incomplete. Place numbers in some of the empty cells below so that in total the grid 
# contains one 1, two 2’s, etc., up to seven 7’s. Furthermore, each row and column must contain 
# exactly 4 numbers which sum to 20. Finally, the numbered cells must form a connected region*, 
# but every 2-by-2 subsquare in the completed grid must contain at least one empty cell.

# The answer to this puzzle is the product of the areas of the connected groups of empty squares in the completed grid.

from z3 import *
from functools import reduce
import time

import constraints
import helper

tfs_array = (
    (0, 4, 0, 0, 0, 0, 0),
    (0, 0, 6, 3, 0, 0, 6),
    (0, 0, 0, 0, 0, 5, 5),
    (0, 0, 0, 4, 0, 0, 0),
    (4, 7, 0, 0, 0, 0, 0),
    (2, 0, 0, 7, 4, 0, 0),
    (0, 0, 0, 0, 0, 1, 0),
)

def one_to_seven(grid, c):
    s_grid_size = 7

    c.add(constraints.findNNs(grid,s_grid_size))

def row_col_four_twenty(grid, c):
    constraints.sum_of_rows(grid, c, 20)
    constraints.count_in_each_r_and_c(grid, c, 4)

s = Solver()

X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(7)] for i in range(7)]

one_to_seven(X, s)
row_col_four_twenty(X, s)

constraints.check_n_by_n_subgrid_empty_space(X, s, 2, 1)
constraints.check_within_range(X, s, 0, 7)

tfs_array_constr = [
    If(tfs_array[i][j] == 0, True, X[i][j] == tfs_array[i][j])
    for i in range(7)
    for j in range(7)
]

s.add(tfs_array_constr)

def calculate_answer(grid):
   print("Final Answer : ")
   print(reduce((lambda x,y: x*y), helper.count_region(grid, count_zero=True)))
   print("Execution Complete!!")

# enforce_cell_neighbours(X, s)
stats_to_print = ["decisions", "solve-eqs-steps",
                  "time", "num allocs", "memory"]
start_time = time.time_ns()
while True:
    if s.check() == sat:
        print("------------------------")
        # print(s.statistics().keys())
        m = s.model()
        print("stats for this run")
        stats = s.statistics()
        for stat in stats_to_print:
            if stat in stats.keys():
                print(stat, stats.get_key_value(stat))

        r = [[m.evaluate(X[i][j]).as_long() for j in range(7)] for i in range(7)]
        if len(helper.count_region(r, count_zero=False))==1:
            print("found solution")
            print_matrix(r)
            calculate_answer(r)
            break
        else:
            print("rerun")
            new_c = Not(And([X[i][j] == r[i][j]
                        for i in range(7) for j in range(7)]))
            s.add(new_c)

    else:
        print("failed to solve")
        break

end_time = time.time_ns()

print("elapsed time:", end_time-start_time)