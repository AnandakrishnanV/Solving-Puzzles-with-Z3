from z3 import *

s = Solver()

x = Int("price")
y = Int("qty")

s.add(4 * x == 20)
s.add(x * y == 40)

s.check()

print(s.model())


X = [[
    Int("x_%s_%s" % (i+1, j+1)) for j in range(9)
    ] for i in range(9)]

# each cell must between 1-9
cells_c = [And(1 <= X[i][j], X[i][j]<=9)
           for i in range(9) for j in range(9)]

rows_c= [Distinct(X[i]) for i in range(9)]

cols_c   = [ Distinct([ X[i][j] for i in range(9) ]) 
             for j in range(9) ]


sq_c = [ Distinct([ X[3*i0 + i][3*j0 + j] 
                        for i in range(3) for j in range(3) ]) 
             for i0 in range(3) for j0 in range(3) ]

sudoku_c = cells_c + rows_c + cols_c + sq_c

instance = ((5,3,0,0,7,0,0,0,0),
            (6,0,0,1,9,5,0,0,0),
            (0,9,8,0,0,0,0,6,0),
            (8,0,0,0,6,0,0,0,3),
            (4,0,0,8,0,3,0,0,1),
            (7,0,0,0,2,0,0,0,6),
            (0,6,0,0,0,0,2,8,0),
            (0,0,0,4,1,9,0,0,5),
            (0,0,0,0,8,0,0,7,9))

instance_c = [ If(instance[i][j] == 0, 
                  True, 
                  X[i][j] == instance[i][j]) 
               for i in range(9) for j in range(9) ]


s = Solver()                                            # (1)
s.add(sudoku_c + instance_c)                            # (2)
if s.check() == sat:                                    # (3)
    m = s.model()                                       # (4)
    r = [ [ m.evaluate(X[i][j]) for j in range(9) ]     # (5)
          for i in range(9) ]
    print_matrix(r)                                     # (6)
else:
    print("failed to solve")                            # (7)
