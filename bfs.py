from collections import deque

t1 = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
t2 = [[1, 1, 0], [1, 1, 0], [0,1, 0]]


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


print(is_fully_connected(t1))
print(is_fully_connected(t2))