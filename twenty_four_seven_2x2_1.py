# Jane Street: March 2019
# Twenty Four Seven 2-by-2 #1

# Each of the grids above is incomplete. Place numbers in some of the empty cells so that in total 
# each grid’s interior contains one 1, two 2’s, etc., up to seven 7’s. Furthermore, each row and column 
# within each grid must contain exactly 4 numbers which sum to 20. Finally, the numbered cells must form 
# a connected region, but every 2-by-2 subsquare in the completed grid must contain at least one empty cell.

# Some numbers have been placed inside each grid. Additionally, some numbers have been placed outside of 
# the grids. These numbers indicate the first value seen in the corresponding row or column when looking 
# into the grid from that location.

# Once each of the grids is complete, create a 7-by-7 grid by “adding” the four grids’ interiors together 
# (as if they were 7-by-7 matrices). The answer to this month’s puzzle is the sum of the squares of the values in this final grid.

from z3 import *
import time

import constraints
import helper

tfs_array_one = (
    (0, 7, 6, 0, 0, 0, 0),
    (0, 0, 0, 6, 6, 0, 0),
    (5, 0, 0, 0, 0, 0, 0),
    (0, 6, 0, 0, 0, 4, 0),
    (0, 0, 0, 0, 0, 0, 6),
    (0, 0, 4, 7, 0, 0, 0),
    (0, 0, 0, 0, 7, 7, 0),
)

rc_left_one = [0, 3, 0, 0, 5, 0, 1]
rc_right_one = [4, 0, 4, 0, 0, 2, 0]

cc_top_one = [0, 0, 0, 0, 0, 5, 7]
cc_bottom_one = [7, 2, 0, 0, 0, 0, 0]

tfs_array_two = (
    (0, 0, 4, 0, 0, 0, 0),
    (0, 4, 0, 0, 0, 0, 0),
    (4, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 7),
    (0, 0, 0, 0, 0, 5, 0),
    (0, 0, 0, 0, 7, 0, 0),
)

rc_left_two = [0, 0, 0, 2, 6, 3, 0]
rc_right_two = [0, 4, 3, 5, 0, 0, 0]

cc_top_two = [0, 0, 0, 6, 3, 7, 0]
cc_bottom_two = [0, 3, 6, 7, 0, 0, 0]

tfs_array_three = (
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
)

rc_left_three = [4, 6, 5, 7, 5, 2, 7]
rc_right_three = [3, 6, 3, 3, 7, 6, 7]

cc_top_three = [6, 4, 4, 6, 7, 3, 3]
cc_bottom_three = [2, 6, 7, 7, 2, 4, 7]

tfs_array_four = (
    (0, 0, 0, 7, 0, 0, 0),
    (5, 0, 0, 0, 0, 6, 0),
    (0, 0, 2, 0, 0, 0, 0),
    (5, 0, 0, 0, 0, 0, 7),
    (0, 0, 0, 0, 7, 0, 0),
    (0, 7, 0, 0, 0, 0, 3),
    (0, 0, 0, 6, 0, 0, 0),
)

rc_left_four = [5, 0, 0, 0, 4, 0, 0]
rc_right_four = [0, 0, 7, 0, 0, 0, 4]

cc_top_four = [5, 0, 5, 0, 2, 0, 7]
cc_bottom_four = [4, 0, 6, 0, 4, 0, 3]


question_array = [tfs_array_one, tfs_array_two, tfs_array_three, tfs_array_four]
top_array = [cc_top_one, cc_top_two, cc_top_three, cc_top_four]
bottom_array = [cc_bottom_one, cc_bottom_two, cc_bottom_three, cc_bottom_four]
right_array = [rc_right_one, rc_right_two, rc_right_three, rc_right_four]
left_array = [rc_left_one, rc_left_two, rc_left_three, rc_left_four]


s = Solver()
Xs = []

grid_size = 7

for n in range(4):
    Xs.append(
        [[Int("x_%s_%s_%s" % (n, i + 1, j + 1)) for j in range(7)] for i in range(7)]
    )

def final_constraint(Xs):
    ROWS = 7
    COLS = 7
    new_sum = [[None for i in range(ROWS)] for j in range(COLS)]
    for i in range(ROWS):
        for j in range(COLS):
            new_sum[i][j] = Sum([X[i][j] for X in Xs])
    constraints.check_within_range(new_sum, s, 0, 28)
    constraints.sum_of_rows(new_sum, s, 80)


for index, x in enumerate(Xs):
    s.add(constraints.findNNs(x, 7))
    constraints.check_within_range(x, s, 0, 7)
    constraints.sum_of_rows(x, s, 20)
    constraints.count_in_each_r_and_c(x, s, 4)
    constraints.check_n_by_n_subgrid_empty_space(x, s, 2, 1)

    tfs_array_constr = [
        If(
            question_array[index][i][j] == 0,
            True,
            x[i][j] == question_array[index][i][j],
        )
        for i in range(7)
        for j in range(7)
    ]
    s.add(tfs_array_constr)

    constraints.blue_constraints(
        x,
        s,
        7,
        3,
        left_array[index],
        right_array[index],
        top_array[index],
        bottom_array[index],
        if_only_first=True,
    )
final_constraint(Xs)


stats_to_print = ["decisions", "solve-eqs-steps", "time", "num allocs", "memory"]
start_time = time.time_ns()
while True:
    if s.check() == sat:
        print("------------------------")
        m = s.model()
        print("stats for this run")
        stats = s.statistics()
        for stat in stats_to_print:
            if stat in stats.keys():
                print(stat, stats.get_key_value(stat))
        all_connected = True
        
        for X in Xs:
            r = [[m.evaluate(X[i][j]).as_long() for j in range(7)] for i in range(7)]
            if len(helper.count_region(r, count_zero=False)) == 1:
                pass
            else:
                all_connected = False
                new_c = Not(And([X[i][j] == r[i][j] for i in range(7) for j in range(7)]))
                s.add(new_c)

        if all_connected:
            print("found solution")
            res = sum([sum([m.evaluate(X[i][j]).as_long() for X in Xs])**2 for j in range(7) for i in range(7)])

            for X in Xs:
                r = [
                    [m.evaluate(X[i][j]).as_long() for j in range(7)] for i in range(7)
                ]
                print_matrix(r)
                print("-------")
            print("res= ",res)
            break
        else:
            print("rerun")
            s.add(new_c)

    else:
        print("failed to solve")
        break

end_time = time.time_ns()

print("elapsed time:", end_time - start_time)
