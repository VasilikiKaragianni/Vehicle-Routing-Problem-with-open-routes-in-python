from Solver import *

m = Model ()
m.BuildModel()
s = Solver(m)
s.ApplyNearestNeighborMethod()
print(s.objective())