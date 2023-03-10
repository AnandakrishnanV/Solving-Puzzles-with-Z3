from z3 import *
s = Solver()




x = Int('X')
y = Int('Y')
B = [Bool("b_%s"%(i)) for i in range(5)]


A = [0,0,1,2,3]
X = [Int("X_%s"%i) for i in range(5)]

for xx in X:
    c= If(xx!=0 and y ==0, y==xx,True)
# for i in X:
#     s.add(X[i] == A[i])
# print(B)
# cs = []
# for i in range(5):
#     c = If(y==i,B[i]==True,True)
#     cs.append(c)
# c = If(x==5,y==2,y==1)
# cs.append(c)


s.add(cs)
if s.check() == sat:
    print(s.model())
else:
    print("failed to solve")
