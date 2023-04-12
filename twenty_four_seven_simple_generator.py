from z3 import *
from functools import reduce
import time
import random
import numpy as np

import constraints
import helper

tfs_array = (
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
)

dict_count = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0
}

iteration_count = 0


def one_to_seven(grid, c):
    s_grid_size = 7

    return constraints.findNNs(grid, s_grid_size)


def row_col_four_twenty(grid, c):
    constraints.sum_of_rows(grid, c, 20)
    constraints.count_in_each_r_and_c(grid, c, 4)



def add_tfs_constraint(grid, s):
    input_array = np.zeros((7, 7))
    number_counts = copy.deepcopy(dict_count)

    tfs_array_constr = []
    for i in range(7):
        for j in range(7):
            if random.randint(1, 9) == 2:

                number_set = False
                while not number_set:
                    new_number = random.randint(1, 7)
                    if number_counts[new_number] < new_number:
                        tfs_array_constr.append(
                            If(random.randint(1, 7) == 0, True, grid[i][j] == tfs_array[i][j]))
                        input_array[i][j] = new_number
                        number_set = True
                        number_counts[new_number] += 1
            else:
                tfs_array_constr.append(
                    If(tfs_array[i][j] == 0, True, grid[i][j] == tfs_array[i][j]))

    print("generating a new random matrix")
    return tfs_array_constr


def calculate_answer(grid):
    print("Final Answer : ")
    print(reduce((lambda x, y: x*y), helper.count_region(grid, count_zero=True)))
    print("Execution Complete!!")


def check_sat(grid, s):
    # enforce_cell_neighbours(X, s)
    stats_to_print = ["decisions", "solve-eqs-steps",
                      "time", "num allocs", "memory"]
    start_time = time.time_ns()
    while True:
        if s.check() == sat:
            m = s.model()

            r = [[m.evaluate(grid[i][j]).as_long() for j in range(7)]
                 for i in range(7)]
            #one or two connected regions
            if len(helper.count_region(r, count_zero=False)) < 3:
                print("found solution")
                print_matrix(r)
                calculate_answer(r)
                break
            else:
                new_c = Not(And([grid[i][j] == r[i][j]
                            for i in range(7) for j in range(7)]))
                s.add(new_c)

        else:
            print("failed to solve")
            print("setting new random integers")
            set_grid()

    end_time = time.time_ns()

    duration_nanoseconds = end_time-start_time
    print("elapsed time:", duration_nanoseconds)
    duration_minutes = duration_nanoseconds / (60 * 1e9)
    print("elapsed time:", duration_minutes)


def set_grid():

    s = Solver()

    X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(7)] for i in range(7)]

    s.add(one_to_seven(X, s))
    row_col_four_twenty(X, s)

    constraints.check_n_by_n_subgrid_empty_space(X, s, 2, 1)
    constraints.check_within_range(X, s, 0, 7)

    s.add(add_tfs_constraint(X, s))
    check_sat(X, s)


# start generator
set_grid()
