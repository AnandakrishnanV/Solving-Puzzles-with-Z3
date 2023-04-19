# Jane Street: February 2023
# Twenty Four Seven (Four-in-One)

# Four Twenty Four Seven grids have been smooshified together within the 12-by-12 grid above.

# Place numbers in some of the empty cells so that in total each of the four 7-by-7 outlined grids is a legal 
# “Twenty Four Seven” grid. Namely: each 7-by-7 grid’s interior should contain one 1, two 2’s, etc., up to seven 7’s. 
# Furthermore, each row and column within the 7-by-7’s must contain exactly 4 numbers which sum to 20. Finally, 
# the numbered cells must form a connected region, but every 2-by-2 subsquare in the completed grid must contain at least one empty cell.

# Some numbers have been placed inside the grid. Additionally, some blue numbers have been placed outside the grid. 
# A number outside the grid represents either the sum of the row or column it is facing, or the value of the first number it sees in that row or column.

# Once completed, you can submit as your answer the product of the areas of the connected groups of orthogonally adjacent empty squares in the grid.


from z3 import *
from functools import reduce
import time

import constraints
import helper
# ==================================
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

# =================================

def one_to_seven(grid, c):
    starting_point = [0, 5]
    s_grid_size = 7

    # for finding 1 1s to 7 7s
    grid_number_c = []
    for i0 in starting_point:
        for j0 in starting_point:
            i1 = i0+s_grid_size
            j1 = j0+s_grid_size
            grid_number_c += constraints.findNNs([row[j0:j1] for row in grid[i0:i1]],s_grid_size)

    c.add(grid_number_c)


def row_col_four_twenty(grid, c):
    constraints.sum_of_rows([row[:7] for row in grid[:7]], c, 20)
    constraints.count_in_each_r_and_c([row[:7] for row in grid[:7]], c, 4)

    constraints.sum_of_rows([row[5:] for row in grid[:7]], c, 20)
    constraints.count_in_each_r_and_c([row[5:] for row in grid[:7]], c, 4)

    constraints.sum_of_rows([row[:7] for row in grid[5:]], c,20)
    constraints.count_in_each_r_and_c([row[:7] for row in grid[5:]], c, 4)

    constraints.sum_of_rows([row[5:] for row in grid[5:]], c,20)
    constraints.count_in_each_r_and_c([row[5:] for row in grid[5:]], c, 4)

s = Solver()

X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(12)] for i in range(12)]

one_to_seven(X, s)
row_col_four_twenty(X, s)

constraints.blue_constraints(X, s, 12, 3, row_constr_left, row_constr_right, column_constr_top, column_constr_bottom, False)
constraints.check_n_by_n_subgrid_empty_space(X, s, 2, 1)
constraints.check_within_range(X, s, 0, 7)

tfs_array_constr = [
    If(tfs_array[i][j] == 0, True, X[i][j] == tfs_array[i][j])
    for i in range(12)
    for j in range(12)
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

        r = [[m.evaluate(X[i][j]).as_long() for j in range(12)] for i in range(12)]
        if len(helper.count_region(r, count_zero=False))==1:
            print("found solution")
            print_matrix(r)
            calculate_answer(r)
            break
        else:
            print("rerun")
            new_c = Not(And([X[i][j] == r[i][j]
                        for i in range(12) for j in range(12)]))
            s.add(new_c)

    else:
        print("failed to solve")
        break

end_time = time.time_ns()

print("elapsed time:", end_time-start_time)

# stats
# (:added-eqs                   920973
#  :arith-eq-adapter            17514
#  :arith-bound-propagations-lp 107775
#  :arith-conflicts             690
#  :arith-diseq                 435864
#  :arith-fixed-eqs             17865
#  :arith-lower                 884119
#  :arith-make-feasible         30799
#  :arith-max-columns           1805
#  :arith-max-rows              412
#  :arith-offset-eqs            42545
#  :arith-upper                 440466
#  :binary-propagations         1821976
#  :conflicts                   2202
#  :decisions                   18672
#  :del-clause                  16466
#  :final-checks                1
#  :max-memory                  35.82
#  :memory                      21.80
#  :minimized-lits              19228
#  :mk-bool-var                 36447
#  :mk-clause                   23229
#  :mk-clause-binary            22257
#  :num-allocs                  131945840
#  :num-checks                  1
#  :propagations                2022302
#  :restarts                    18
#  :rlimit-count                8143703
#  :solve-eqs-elim-vars         21
#  :solve-eqs-steps             21
#  :time                        2.97)
