from z3 import *

s = Solver()
test_array = ((1, 0, 0), (0, 0, 0), (0, 0, 1))
X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(3)] for i in range(3)]
B = [[Bool("b_%s_%s" % (i + 1, j + 1)) for j in range(3)] for i in range(3)]
Found = Bool("found")
tfs_c = [
    If(test_array[i][j] == 0, True, X[i][j] == test_array[i][j])
    for i in range(3)
    for j in range(3)
]

cell_c = [And(0 <= X[i][j], X[i][j] <= 1) for i in range(3) for j in range(3)]

def findNeighbours(X, i, j):
    nbs = []
    max = len(X)
    if i>0:
        nbs.append(X[i-1][j])
    if j>0:
        nbs.append(X[i][j-1])
    if i<max-1:
        nbs.append(X[i+1][j])
    if j<max-1:
        nbs.append(X[i][j+1])
    return nbs

for i in range(3):
    for j in range(3):
        Implies(X[i][j]!=0, findNeighbours(X,i,j))





s.add(tfs_c+cell_c)
if s.check() == sat:
    m = s.model()
    r = [[m.evaluate(X[i][j]) for j in range(3)] for i in range(3)]
    print_matrix(r)
else:
    print("failed to solve")



# def add_random_numbers(matrix, n):

#     number_counts = copy.deepcopy(dict_count)

#     array_tuple = np.array(matrix)

#     for i in range(n):
#         x = random.randint(0, len(matrix)-1)
#         y = random.randint(0, len(matrix[0])-1)

    # number_set = False
    # while not number_set:
    #     new_number = random.randint(1, 7)
    #     if number_counts[new_number] < new_number:
    #         array_tuple[x][y] = new_number
    #         number_set = True
    #         number_counts[new_number] += 1

#     matrix = tuple(map(tuple, array_tuple))
#     return matrix


# def add_tfs_constraint(grid, c):
#     new_tfs = copy.deepcopy(tfs_array)
#     new_tfs_tuple = add_random_numbers(new_tfs, 1)
#     my_ints = [[Int(str(j)) for j in i] for i in new_tfs_tuple]
#     print_matrix(my_ints)
#     time.sleep(5)
#     tfs_array_constr = [
#         If(my_ints[i][j] == 0, True, grid[i][j] == my_ints[i][j])
#         for i in range(7)
#         for j in range(7)
#     ]

#     return tfs_array_constr