from Solver import *

m = Model()
m.BuildModel()
s = Solver(m)
solution = s.ApplyNearestNeighborMethod()
print(s.objective(solution))
for rout in solution.routes:
    sdem = 0
    for nod in rout.sequenceOfNodes:
        sdem += nod.demand
    print('sdem- ' + str(sdem))
    print('rout.load- ' + str(rout.load))
# solution2 = s.LocalSearch()
# print(s.objective(solution2))
# for rout in solution2.routes:
#     sdem = 0
#     for nod in rout.sequenceOfNodes:
#         sdem += nod.demand
#     print('sdem- ' + str(sdem))
#     print('rout.load- ' + str(rout.load))
solution3 = s.VND()
print(s.objective(solution3))
for rout in solution3.routes:
    sdem = 0
    for nod in rout.sequenceOfNodes:
        sdem += nod.demand
    print('sdem- ' + str(sdem))
    print('rout.load- ' + str(rout.load))

