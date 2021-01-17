from Solver import *


class RelocationMove(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = None

    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = 10 ** 9


class Solver:
    def __init__(self, m, s):
        self.allNodes = m.allNodes
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.distance
        self.timeMatrix = m.time
        self.capacity = m.capacity
        self.sol = s.sol
        self.bestSolution = s.sol
        self.overallBestSol = None
        self.repetitions = 0

    def solve(self):

        self.LocalSearch(0)
        if self.overallBestSol == None or self.overallBestSol.cost > self.sol.cost:
            self.overallBestSol = self.cloneSolution(self.sol)
        print(' Before LS:', self.sol.cost, 'BestOverall: ', self.overallBestSol.cost)

        self.ReportSolution(self.overallBestSol)
        # SolDrawer.draw(10000, self.sol, self.allNodes)
        return self.overallBestSol



    def LocalSearch(self, operator):
        # self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        localSearchIterator = 0

        rm = RelocationMove()

        while terminationCondition is False:

            self.InitializeOperators(rm)
            # , sm, top
            # SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)

            # Relocations
            if operator == 0:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True


            self.TestSolution()

            if (self.sol.cost < self.bestSolution.cost):
                self.bestSolution = self.cloneSolution(self.sol)

            localSearchIterator = localSearchIterator + 1

        self.sol = self.bestSolution
        self.repetitions = localSearchIterator

    def cloneRoute(self, rt: Route):
        capacity = rt.capacity
        cloned = Route(capacity)
        cloned.distance = rt.distance
        cloned.time = rt.time
        cloned.load = rt.load
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        return cloned

    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        for i in range(0, len(self.sol.sol.routes)):
            rt = self.sol.sol.routes[i]
            clonedRoute = self.cloneRoute(rt)
            cloned.routes.append(clonedRoute)
        cloned.cost = self.sol.cost
        return cloned

    def FindBestRelocationMove(self, rm):
        for originRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[originRouteIndex]
            for targetRouteIndex in range(0, len(self.sol.routes)):
                rt2: Route = self.sol.routes[targetRouteIndex]
                for originNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                    for targetNodeIndex in range(0, len(rt2.sequenceOfNodes) - 1):

                        if originRouteIndex == targetRouteIndex and (
                                targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.sequenceOfNodes[originNodeIndex - 1]
                        B = rt1.sequenceOfNodes[originNodeIndex]
                        C = rt1.sequenceOfNodes[originNodeIndex + 1]

                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        G = rt2.sequenceOfNodes[targetNodeIndex + 1]

                        if rt1 != rt2:
                            if rt2.load + B.demand > rt2.capacity:
                                continue

                        costAdded = self.distanceMatrix[A.id][C.id] + self.distanceMatrix[F.id][B.id] + \
                                    self.distanceMatrix[B.id][G.id]
                        costRemoved = self.distanceMatrix[A.id][B.id] + self.distanceMatrix[B.id][C.id] + \
                                      self.distanceMatrix[F.id][G.id]

                        originRtCostChange = self.distanceMatrix[A.id][C.id] - self.distanceMatrix[A.id][B.id] - \
                                             self.distanceMatrix[B.id][C.id]
                        targetRtCostChange = self.distanceMatrix[F.id][B.id] + self.distanceMatrix[B.id][G.id] - \
                                             self.distanceMatrix[F.id][G.id]

                        originRtTimeChange = self.timeMatrix[A.id][C.id] - self.timeMatrix[A.id][B.id] - \
                                             self.timeMatrix[B.id][C.id]
                        targetRtTimeChange = self.timeMatrix[F.id][B.id] + self.timeMatrix[B.id][G.id] - \
                                             self.timeMatrix[F.id][G.id]


                        if rt1 != rt2:
                            rt1time = rt1.time + originRtTimeChange
                            rt2time = rt2.time + targetRtTimeChange
                            if rt1.time + originRtTimeChange > 3.5:
                                continue
                            if rt2.time + targetRtTimeChange > 3.5:
                                continue
                        if rt1 == rt2:
                            rtfull = rt1.time + originRtTimeChange + targetRtTimeChange
                            if rt1.time + originRtTimeChange + targetRtTimeChange > 3.5:
                                continue

                        moveCost = costAdded - costRemoved

                        if(moveCost < 0):
                            if (moveCost < rm.moveCost):
                                self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex,
                                                             targetNodeIndex, moveCost, originRtCostChange,
                                                             targetRtCostChange, rm)

    def ApplyRelocationMove(self, rm: RelocationMove):

        oldCost = self.CalculateTotalCost(self.sol)

        originRt = self.sol.routes[rm.originRoutePosition]
        targetRt = self.sol.routes[rm.targetRoutePosition]

        B = originRt.sequenceOfNodes[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition, B)
            else:
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)

            originRt.distance += rm.moveCost
        else:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt.distance += rm.costChangeOriginRt
            targetRt.distance += rm.costChangeTargetRt
            originRt.load -= B.demand
            targetRt.load += B.demand

        self.sol.cost += rm.moveCost

        newCost = self.CalculateTotalCost(self.sol)
        # debuggingOnly
        if abs((newCost - oldCost) - rm.moveCost) > 0.0001:
            print('Cost Issue')


    def ReportSolution(self, sol):
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ')
            print(rt.cost)
        print(self.sol.cost)



    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost,
                                originRtCostChange, targetRtCostChange, rm: RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost

    def CalculateTotalCost(self, sol):
        c = 0
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes) - 1):
                a = rt.sequenceOfNodes[j]
                b = rt.sequenceOfNodes[j + 1]
                c += self.distanceMatrix[a.id][b.id]
        return c

    def InitializeOperators(self, rm):
        rm.Initialize()




    def TestSolution(self):
        totalSolCost = 0
        for r in range(0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            rtCost = 0
            rtLoad = 0
            for n in range(0, len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[n]
                B = rt.sequenceOfNodes[n + 1]
                rtCost += self.distanceMatrix[A.id][B.id]
                rtLoad += A.demand
            if abs(rtCost - rt.distance) > 0.0001:
                print('Route Distance Cost problem')
            if rtLoad != rt.load:
                print('Route Load problem')

            totalSolCost += rt.distance

        if abs(totalSolCost - self.sol.cost) > 0.0001:
            print('Solution Cost problem')

