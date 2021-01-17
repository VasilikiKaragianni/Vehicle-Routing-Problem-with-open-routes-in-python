from Solver import *

m = Model ()
m.BuildModel()
s = Solver(m)
solution = s.ApplyNearestNeighborMethod()
s.objective(solution)
s.LocalSearch()