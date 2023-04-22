# Implements each constraint as a resuable function

from z3 import *
from helper import *

# grid: Input NxN grid
# c:z3 solver object
# low: Lowest allowed value in the grid 
# high: Highest allowed value in the grid

# Sets conditions for allowed numbers in the grid

def check_within_range(grid, c, low, high):
    if not grid or not grid[0]:
        return
    ROWS = len(grid)
    COLS = len(grid[0])

    cell_c = [
        And(low <= grid[i][j], grid[i][j] <= high) for i in range(ROWS) for j in range(COLS)
    ]

    c.add(cell_c)

# grid: Input NxN grid
# max_n: grid size (7 for 7x7)

# Sets conditions for 1x1, 2x2...NxN

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


# grid: Input NxN grid
# c:z3 solver object
# count: Number of required elements in each row/column 

# Sets conditions for 'count' number of elements in each row/column 

def count_in_each_r_and_c(grid, c, count):
    if not grid or not grid[0]:
        return
    ROWS = len(grid)
    COLS = len(grid[0])
    for i in range(ROWS):
        c.add(Sum([If(grid[i][j] != 0, 1, 0) for j in range(COLS)]) == count)
    for j in range(COLS):
        c.add(Sum([If(grid[i][j] != 0, 1, 0) for i in range(ROWS)]) == count)

# grid: Input NxN grid
# c:z3 solver object
# target_sum: Sum of elements in each row/column 

# Sets conditions for 'target_sum' sum of elements in each row/column 

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

# grid: Input NxN grid
# c:z3 solver object
# target_sum: Sum of elements in each row/column 
# subgrid_size: Size of subgrid square to enforce condition (enforced on every possible subgrid of this size in the grid)
# min_empty: Minimum number of cells that should be empty in the subgrid

# Sets conditions for enforcing that each subgrid of 'subgrid_size' should have atleast 'min_empty' cells as empty(0)

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

# grid: Input NxN grid
# c:z3 solver object
# n: Size of the Problem gird
# z: Maximum Number of allowed empty spaces in the individual NxN grid (i.e for a 7x7 based problem set, with 4 allowed values per row/column, this value will be 3) 
# row_constr_left: Blue number/ Numbers outside the grid that represent either sum or first number encountered in respective row/column, along the left edge of the grid
# row_constr_right: Blue number/ Numbers outside the grid that represent either sum or first number encountered in respective row/column, along the right edge of the grid
# column_constr_top: Blue number/ Numbers outside the grid that represent either sum or first number encountered in respective row/column, along the top edge of the grid
# column_constr_bottom: Blue number/ Numbers outside the grid that represent either sum or first number encountered in respective row/column, along the bottom edge of the grid
# if_only_first: Boolean representing checking condition of thhe 4 constrs. True: Checks if each of numbers are the first number encountered in the row/column
#                                                                           False: Checks if each of the numbers are either sum or first number encountered in the row/column

# Sets conditions for enforcing that the Blue number/ Numbers outside the grid represent either the sum or first number encountered in its respective row/column

            
def blue_constraints(grid, c, n, z, row_constr_left, row_constr_right, column_constr_top, column_constr_bottom, if_only_first):
    mi = n - 1
    # left vertical
    for i in range(n):
        row_sum = z3.Sum(grid[i])

        # Checking for first non-zero element
        if row_constr_left[i]:
            first_val = z3.If(And(z > 0, grid[i][0] == 0),
                              If(And(z > 1, grid[i][1] == 0),
                                 If(And(z > 2, grid[i][2] == 0),
                                    If(And(z > 3, grid[i][3] == 0),
                                        If(And(z > 4, grid[i][4] == 0),
                                           If(And(
                                               z > 5, grid[i][5] == 0), grid[i][6], grid[i][5]),
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
                                           If(And(
                                               z > 5, grid[i][mi-5] == 0), grid[i][mi-6], grid[i][mi-5]),
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
                                           If(And(
                                               z > 5, grid[5][j] == 0), grid[6][j], grid[5][j]),
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
                                           If(And(
                                               z > 5, grid[mi-5][j] == 0), grid[mi-6][j], grid[mi-5][j]),
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
