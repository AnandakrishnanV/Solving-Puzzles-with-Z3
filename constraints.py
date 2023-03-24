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
            c.add(Implies(grid[i][j] != 0, Or([k != 0 for k in get_neighbours(grid, i, j)])))


def check_within_range(grid, c, low, high):
    if not grid or not grid[0]:
        return
    ROWS = len(grid)
    COLS = len(grid[0])

    cell_c = [
        And(low <= grid[i][j], grid[i][j] <= high) for i in range(ROWS) for j in range(COLS)
    ]

    c.add(cell_c)

