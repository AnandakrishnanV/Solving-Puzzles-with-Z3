from collections import deque


def get_neighbours(grid, i, j):
    nb = []
    if i > 0:
        nb.append(grid[i - 1][j])
    if i < len(grid) - 1:
        nb.append(grid[i + 1][j])
    if j > 0:
        nb.append(grid[i][j - 1])
    if j < len(grid[0]) - 1:
        nb.append(grid[i][j + 1])
    return nb


# def is_fully_connected(matrix):
#     rows, cols = len(matrix), len(matrix[0])
#     visited = [[False] * cols for _ in range(rows)]
#     q = deque()
#     connected_components = 0

#     for i in range(rows):
#         for j in range(cols):
#             if matrix[i][j] >= 1 and not visited[i][j]:
#                 # Start a new connected component
#                 connected_components += 1
#                 q.append((i, j))
#                 visited[i][j] = True
#                 while q:
#                     x, y = q.popleft()
#                     # Visit all the neighbors of the current cell
#                     for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
#                         nx, ny = x + dx, y + dy
#                         if (
#                             0 <= nx < rows
#                             and 0 <= ny < cols
#                             and matrix[nx][ny] >= 1
#                             and not visited[nx][ny]
#                         ):
#                             q.append((nx, ny))
#                             visited[nx][ny] = True

#     # Check if there is only one connected component
#     return connected_components == 1


def count_region(matrix, count_zero):
    rows, cols = len(matrix), len(matrix[0])
    visited = [[False] * cols for _ in range(rows)]
    q = deque()
    connected_components = 0
    len_connected_components = []

    for i in range(rows):
        for j in range(cols):

            matching_grid = (count_zero and matrix[i][j] == 0) or (
                not count_zero and matrix[i][j] > 0
            )
            if matching_grid and not visited[i][j]:
                # Start a new connected component
                connected_components += 1
                q.append((i, j))
                visited[i][j] = True
                counter = 0
                while q:
                    x, y = q.popleft()
                    counter = counter + 1
                    # Visit all the neighbors of the current cell
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = x + dx, y + dy

                        if (
                            0 <= nx < rows
                            and 0 <= ny < cols
                            and (
                                (count_zero and matrix[nx][ny] == 0)
                                or (not count_zero and matrix[nx][ny] > 0)
                            )
                            and not visited[nx][ny]
                        ):
                            q.append((nx, ny))
                            visited[nx][ny] = True

                len_connected_components.append(counter)
    # Check if there is only one connected component
    return len_connected_components
