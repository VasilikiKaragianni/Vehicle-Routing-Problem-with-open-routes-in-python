from Solver import *

m = Model ()
m.BuildModel()
s = Solver(m)
solution = s.ApplyNearestNeighborMethod()
print(s.objective(solution))
solution2 = s.LocalSearch()
print(s.objective(solution2))
# solution3 = s.VND()
# print(s.objective(solution3))
