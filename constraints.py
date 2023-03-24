from z3 import *
from helper import *


def findNNs(grid, max_n):
    if not grid or not grid[0]:
        return
    ROWS = len(grid)
    COLS = len(grid[0])

    cells = [grid[i][j] for i in range(ROWS) for j in range(COLS)]

    grid_number_c = []
    for n in range(1, 1 + max_n):
        s = Sum([If(c == n, 1, 0) for c in cells]) == n
        grid_number_c.append(s)
    return grid_number_c


def count_in_each_r_and_c(grid, c, count):
    if not grid or not grid[0]:
        return
    ROWS = len(grid)
    COLS = len(grid[0])
    for i in range(ROWS):
        c.add(Sum([If(grid[i][j] != 0, 1, 0) for j in range(COLS)]) == count)
    for j in range(COLS):
        c.add(Sum([If(grid[i][j] != 0, 1, 0) for i in range(ROWS)]) == count)


def sum_of_rows(grid, c, target_sum):
    if not grid or not grid[0]:
        return
    ROWS = len(grid)
    COLS = len(grid[0])
    for i in range(ROWS):
        c.add(Sum([If(grid[i][j] != 0, grid[i][j], 0)
              for j in range(COLS)]) == target_sum)
    for j in range(COLS):
        c.add(Sum([If(grid[i][j] != 0, grid[i][j], 0)
              for i in range(ROWS)]) == target_sum)


def check_n_by_n_subgrid_empty_space(grid, c, subgrid_size, min_empty):
    if not grid or not grid[0]:
        return
    ROWS = len(grid)
    COLS = len(grid[0])

    for i in range(ROWS - 1):
        for j in range(COLS - 1):
            cells = [
                grid[k][l]
                for k in range(i, i + subgrid_size)
                for l in range(j, j + subgrid_size)
            ]
            c.add(Sum([If(c == 0, 1, 0) for c in cells]) >= min_empty)


def enforce_cell_neighbours(grid, c):
    for i in range(len(grid)-1):
        for j in range(len(grid)-1):
            c.add(Implies(grid[i][j] != 0, Or(
                [k != 0 for k in get_neighbours(grid, i, j)])))


def check_within_range(grid, c, low, high):
    if not grid or not grid[0]:
        return
    ROWS = len(grid)
    COLS = len(grid[0])

    cell_c = [
        And(low <= grid[i][j], grid[i][j] <= high) for i in range(ROWS) for j in range(COLS)
    ]

    c.add(cell_c)


def blue_constraints(grid, c, n, z, row_constr_left, row_constr_right, column_constr_top, column_constr_bottom, if_only_first):
    mi = n - 1
    # left vertical
    for i in range(n):
        row_sum = z3.Sum(grid[i])

        if row_constr_left[i]:
            first_val = z3.If(And(z > 0, grid[i][0] == 0),
                              If(And(z > 1, grid[i][1] == 0),
                                 If(And(z > 2, grid[i][2] == 0),
                                    If(And(z > 3, grid[i][3] == 0),
                                        If(And(z > 4, grid[i][4] == 0),
                                           If(And(z > 5, grid[i][5] == 0),
                                              If(And(z > 6, grid[i][6] == 0), grid[i][7],grid[i][6]),
                                              grid[i][5]),
                                           grid[i][4]),
                                       grid[i][3]),
                                    grid[i][2],),
                                 grid[i][1],),
                              grid[i][0],
                              )

            if if_only_first:
                c.add(first_val == row_constr_left[i])
            else:
                c.add(
                    Or(first_val == row_constr_left[i], row_sum == row_constr_left[i]))

        if row_constr_right[i]:
            first_val = z3.If(And(z > 0, grid[i][mi-0] == 0),
                              If(And(z > 1, grid[i][mi-1] == 0),
                                 If(And(z > 2, grid[i][mi-2] == 0),
                                    If(And(z > 3, grid[i][mi-3] == 0),
                                        If(And(z > 4, grid[i][mi-4] == 0),
                                           If(And(z > 5, grid[i][mi-5] == 0),
                                              If(And(z > 6, grid[i][mi-6] == 0), grid[i][mi-7], grid[i][mi-6]),
                                              grid[i][mi-5]),
                                           grid[i][mi-4]),
                                       grid[i][mi-3]),
                                    grid[i][mi-2],),
                                 grid[i][mi-1],),
                              grid[i][mi-0],
                              )

            if if_only_first:
                c.add(first_val == row_constr_right[i])
            else:
                c.add(
                    Or(first_val == row_constr_right[i], row_sum == row_constr_right[i]))

    # columns
    for j in range(n):
        col_sum = z3.Sum([grid[i][j] for i in range(n)])

        if column_constr_top[j]:
            first_val = z3.If(And(z > 0, grid[0][j] == 0),
                              If(And(z > 1, grid[1][j] == 0),
                                 If(And(z > 2, grid[2][j] == 0),
                                    If(And(z > 3, grid[3][j] == 0),
                                        If(And(z > 4, grid[4][j] == 0),
                                           If(And(z > 5, grid[5][j] == 0),
                                              If(And(z > 6, grid[6][j] == 0), grid[7][j], grid[6][j]),
                                              grid[5][j]),
                                           grid[4][j]),
                                       grid[3][j]),
                                    grid[2][j],),
                                 grid[1][j],),
                              grid[0][j],
                              )
            if if_only_first:
                c.add(first_val == column_constr_top[j])
            else:
                c.add(
                    Or(first_val == column_constr_top[j],
                       col_sum == column_constr_top[j])
                )

        if column_constr_bottom[j]:
            first_val = z3.If(And(z > 0, grid[mi-0][j] == 0),
                              If(And(z > 1, grid[mi-1][j] == 0),
                                 If(And(z > 2, grid[mi-2][j] == 0),
                                    If(And(z > 3, grid[mi-3][j] == 0),
                                        If(And(z > 4, grid[mi-4][j] == 0),
                                           If(And(z > 5, grid[mi-5][j] == 0),
                                              If(And(z > 6, grid[mi-6][j] == 0), grid[mi-7][j], grid[mi-6][j]),
                                              grid[mi-5][j]),
                                           grid[mi-4][j]),
                                       grid[mi-3][j]),
                                    grid[mi-2][j],),
                                 grid[mi-1][j],),
                              grid[mi-0][j],
                              )
            if if_only_first:
                c.add(first_val == column_constr_bottom[j])
            else:
                c.add(
                    Or(
                        first_val == column_constr_bottom[j],
                        col_sum == column_constr_bottom[j],
                    )
                )
