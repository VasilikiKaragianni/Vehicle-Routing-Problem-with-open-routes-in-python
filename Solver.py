from VRP_Model import *
from SolDrawer import *


class Solution:
    def __init__(self):
        self.cost = 0
        self.routes = []


class RelocationMove(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.originRtTimeChange = None
        self.targetRtTimeChange = None
        self.moveCost = None

    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.originRtTimeChange = None
        self.targetRtTimeChange = None
        self.moveCost = 10 ** 9


class SwapMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = None

    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = 10 ** 9


class TwoOptMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = None

    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10 ** 9


class Solver:
    def __init__(self, m):
        self.allNodes = m.allNodes
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.distance
        self.timeMatrix = m.time
        self.capacity = m.capacity
        self.sol = Solution()
        self.bestSolution = Solution()
        self.route = None
        self.searchTrajectory = []

    def ApplyNearestNeighborMethod(self):

        for t in range(30):
            capacity = 1500
            if t > 14:
                capacity = 1200
                self.route = Route(1200)
            else:
                self.route = Route(1500)
            node = 0
            self.route.sequenceOfNodes.append(self.allNodes[0])
            self.allNodes[0].isRouted = True
            total_demand = 0
            total_time = 0
            total_cost = 0
            position = 0
            while total_demand <= capacity and total_time <= 3.5:
                min1 = 100000000000
                flag = False
                for i in range(len(self.allNodes)):
                    if self.allNodes[i].isRouted == False:
                        flag = True
                        if self.distanceMatrix[node][i] < min1:
                            min1 = self.distanceMatrix[node][i]
                            position = i
                if not flag:
                    break
                elif total_demand + self.allNodes[position].demand <= capacity and total_time + self.timeMatrix[node][
                    position] <= 3.5:
                    self.route.sequenceOfNodes.append(self.allNodes[position])
                    self.allNodes[position].isRouted = True
                    a = self.allNodes[position]
                    total_demand += a.demand
                    total_time += self.timeMatrix[node][position]
                    total_cost += self.distanceMatrix[node][position]
                    node = position
                else:
                    break
            self.route.load = total_demand
            self.route.capacity = capacity
            self.route.time = total_time
            self.route.distance = total_cost
            self.sol.routes.append(self.route)
            self.sol.cost += total_cost

        f = open("NearestNeighbor8180032.txt", "w+")
        for i in range(len(self.sol.routes)):
            rt: Route = self.sol.routes[i]
            f.write("This is route: \n")
            for j in range(len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ', )
                f.write("%d\n" % (rt.sequenceOfNodes[j].ID))
            f.write("\n")
            print("\n")
        solution = self.objective(self.sol)
        f.write("This is the final objective: %d" % (solution))
        f.close()
        SolDrawer.draw('final_Nearest8180032', self.sol, self.allNodes)
        return (self.sol)

    ## method that calculates the total cost of the solution given
    def objective(self, solution):
        total_cost = 0
        single_cost = []
        for i in range(len(solution.routes)):
            cost = 0
            rout: Route = solution.routes[i]
            for j in range(len(rout.sequenceOfNodes) - 1):
                index1 = rout.sequenceOfNodes[j]
                index2 = rout.sequenceOfNodes[j + 1]
                cost += self.distanceMatrix[index1.ID][index2.ID]
            single_cost.append(cost)
            self.sol.routes[i].distance = cost
            total_cost += cost
        return total_cost

    def LocalSearch(self):
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        counter = 0
        rm = RelocationMove()
        localSearchIterator = 0
        while terminationCondition is False:

            # SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)
            self.InitializeRm(rm)
            self.FindBestRelocationMove(rm)
            if rm.originRoutePosition is not None:
                if rm.moveCost < 0:
                    self.ApplyRelocationMove(rm)
                    counter += 1
                else:
                    terminationCondition = True

            self.TestSolution()

            if (self.sol.cost < self.bestSolution.cost):
                self.bestSolution = self.cloneSolution(self.sol)

            localSearchIterator = localSearchIterator + 1

        self.sol = self.bestSolution

        self.TestSolution()
        SolDrawer.draw('final_LS_8180032', self.sol, self.allNodes)

        f = open("LocalSearch8180032.txt", "w+")
        for i in range(len(self.sol.routes)):
            rt: Route = self.sol.routes[i]
            f.write("This is route: \n")
            for j in range(len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ', )
                f.write("%d\n" % (rt.sequenceOfNodes[j].ID))
            f.write("\n")
            print("\n")
        solution = self.objective(self.sol)
        f.write("This is the final objective: %d" % (solution))
        f.close()
        print(counter)

        return (self.sol)


    def cloneRoute(self, rt: Route):
        cloned = Route(rt.capacity)
        cloned.distance = rt.distance
        cloned.load = rt.load
        cloned.time = rt.time
        cloned.distance = rt.distance
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        return cloned

    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            clonedRoute = self.cloneRoute(rt)
            cloned.routes.append(clonedRoute)
        cloned.cost = self.sol.cost
        return cloned

    def FindBestRelocationMove(self, rm):
        for originRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[originRouteIndex]
            for targetRouteIndex in range(0, len(self.sol.routes)):
                rt2: Route = self.sol.routes[targetRouteIndex]
                for originNodeIndex in range(1, len(rt1.sequenceOfNodes)):
                    for targetNodeIndex in range(0, len(rt2.sequenceOfNodes)):

                        if originRouteIndex == targetRouteIndex and (
                                targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.sequenceOfNodes[originNodeIndex - 1]
                        B = rt1.sequenceOfNodes[originNodeIndex]
                        if (rt1.sequenceOfNodes[originNodeIndex] == rt1.sequenceOfNodes[-1]):
                            C = rt1.sequenceOfNodes[originNodeIndex]
                        else:
                            C = rt1.sequenceOfNodes[originNodeIndex + 1]

                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        if (rt2.sequenceOfNodes[targetNodeIndex] == rt2.sequenceOfNodes[-1]):
                            G = rt2.sequenceOfNodes[targetNodeIndex]
                        else:
                            G = rt2.sequenceOfNodes[targetNodeIndex + 1]


                        if (rt1.sequenceOfNodes[originNodeIndex] == rt1.sequenceOfNodes[-1]):
                            if (rt2.sequenceOfNodes[targetNodeIndex] == rt2.sequenceOfNodes[-1]):
                                costAdded = self.distanceMatrix[F.ID][B.ID]
                                costRemoved = self.distanceMatrix[A.ID][B.ID]
                                originRtCostChange = - self.distanceMatrix[A.ID][B.ID]
                                targetRtCostChange = self.distanceMatrix[F.ID][B.ID]
                                originRtTimeChange = - self.timeMatrix[A.ID][B.ID]
                                targetRtTimeChange = self.timeMatrix[F.ID][B.ID]
                            else:
                                costAdded = self.distanceMatrix[F.ID][B.ID] + self.distanceMatrix[B.ID][G.ID]
                                costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[F.ID][G.ID]
                                originRtCostChange = - self.distanceMatrix[A.ID][B.ID]
                                targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.distanceMatrix[B.ID][G.ID] - \
                                                     self.distanceMatrix[F.ID][G.ID]
                                originRtTimeChange = - self.timeMatrix[A.ID][B.ID]
                                targetRtTimeChange = self.timeMatrix[F.ID][B.ID] + self.timeMatrix[B.ID][G.ID] - \
                                                     self.timeMatrix[F.ID][G.ID]

                        elif (rt2.sequenceOfNodes[targetNodeIndex] == rt2.sequenceOfNodes[-1]):
                            costAdded = self.distanceMatrix[A.ID][C.ID] + self.distanceMatrix[F.ID][B.ID]
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID]
                            originRtCostChange = self.distanceMatrix[A.ID][C.ID] - self.distanceMatrix[A.ID][B.ID] - \
                                                 self.distanceMatrix[B.ID][C.ID]
                            targetRtCostChange = self.distanceMatrix[F.ID][B.ID]
                            originRtTimeChange = self.timeMatrix[A.ID][C.ID] - self.timeMatrix[A.ID][B.ID] - \
                                                 self.timeMatrix[B.ID][C.ID]
                            targetRtTimeChange = self.timeMatrix[F.ID][B.ID]

                        else:
                            costAdded = self.distanceMatrix[A.ID][C.ID] + self.distanceMatrix[F.ID][B.ID] + \
                                        self.distanceMatrix[B.ID][G.ID]
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID] + \
                                          self.distanceMatrix[F.ID][G.ID]

                            originRtCostChange = self.distanceMatrix[A.ID][C.ID] - self.distanceMatrix[A.ID][B.ID] - \
                                                 self.distanceMatrix[B.ID][C.ID]
                            targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.distanceMatrix[B.ID][G.ID] - \
                                                 self.distanceMatrix[F.ID][G.ID]
                            originRtTimeChange = self.timeMatrix[A.ID][C.ID] - self.timeMatrix[A.ID][B.ID] - \
                                                 self.timeMatrix[B.ID][C.ID]
                            targetRtTimeChange = self.timeMatrix[F.ID][B.ID] + self.timeMatrix[B.ID][G.ID] - \
                                                 self.timeMatrix[F.ID][G.ID]

                        if rt1 != rt2:
                            if rt2.load + B.demand > rt2.capacity:
                                continue

                        if rt1 != rt2:
                            rt1time = rt1.time + originRtTimeChange
                            rt2time = rt2.time + targetRtTimeChange
                            if rt1time > 3.5:
                                continue
                            if rt2time > 3.5:
                                continue
                        if rt1 == rt2:
                            rtfull = rt1.time + originRtTimeChange + targetRtTimeChange
                            if rtfull > 3.5:
                                continue

                        moveCost = costAdded - costRemoved

                        if (moveCost < rm.moveCost):
                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex,
                                                         targetNodeIndex, moveCost, originRtCostChange,
                                                         targetRtCostChange,
                                                         originRtTimeChange, targetRtTimeChange, rm)

    def ApplyRelocationMove(self, rm: RelocationMove):

        oldCost = self.objective(self.sol)

        originRt = self.sol.routes[rm.originRoutePosition]
        targetRt = self.sol.routes[rm.targetRoutePosition]

        B = originRt.sequenceOfNodes[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition, B)
            else:
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)

            originRt.time += rm.originRtTimeChange + rm.targetRtTimeChange
            originRt.distance += rm.moveCost
        else:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt.distance += rm.costChangeOriginRt
            targetRt.distance += rm.costChangeTargetRt
            originRt.load -= B.demand
            targetRt.load += B.demand
            originRt.time += rm.originRtTimeChange
            targetRt.time += rm.targetRtTimeChange

        self.sol.cost += rm.moveCost

        # This is an alternative way of checking the solution.
        # newCost = self.objective(self.sol)
        # print(newCost,oldCost,rm.moveCost)
        # # debuggingOnly
        # if abs((newCost - oldCost) - rm.moveCost) > 0.0001:
        #     print('Cost Issue')
        self.TestSolution()

    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost,
                                originRtCostChange, targetRtCostChange, originRtTimeChange, targetRtTimeChange,
                                rm: RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost
        rm.originRtTimeChange = originRtTimeChange
        rm.targetRtTimeChange = targetRtTimeChange

    def InitializeOperators(self, rm, sm, top):
        rm.Initialize()
        sm.Initialize()
        top.Initialize()

    def InitializeRm(self, rm):
        rm.Initialize()

    def VND(self):
        self.bestSolution = self.cloneSolution(self.sol)
        VNDIterator = 0
        kmax = 2
        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()
        k = 0
        draw = False

        while k <= kmax:
            self.InitializeOperators(rm, sm, top)
            if k == 2:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None and rm.moveCost < 0:
                    self.ApplyRelocationMove(rm)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.cost)
                    k = 0
                    # print("relocation sol found")
                else:
                    k += 1
                    # print("relocation finished")
                    # print("k is" + str(k))
            elif k == 0:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None and sm.moveCost < 0:
                    self.ApplySwapMove(sm)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.cost)
                    k = 0
                    # print("swap sol found")
                else:
                    k += 1
                    # print("swap finished")
                    # print("k is" + str(k))
            elif k == 1:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None and top.moveCost < 0:
                    self.ApplyTwoOptMove(top)
                    if draw:
                        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.cost)
                    k = 0
                    # print("2opt sol found")
                else:
                    k += 1
                    # print("2opt finished")
                    # print("k is" + str(k))

            if (self.sol.cost < self.bestSolution.cost):
                self.bestSolution = self.cloneSolution(self.sol)

        f = open("VND_8180032.txt", "w+")
        for i in range(len(self.sol.routes)):
            rt: Route = self.sol.routes[i]
            f.write("This is route: \n")
            for j in range(len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ', )
                f.write("%d\n" % (rt.sequenceOfNodes[j].ID))
            f.write("\n")
            print("\n")
        solution = self.objective(self.sol)
        f.write("This is the final objective: %d" % (solution))
        f.close()
        SolDrawer.draw('VND_8180032', self.bestSolution, self.allNodes)
        SolDrawer.drawTrajectory(self.searchTrajectory)
        return (self.sol)

    def FindBestSwapMove(self, sm):
        for firstRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[firstRouteIndex]
            for secondRouteIndex in range(firstRouteIndex, len(self.sol.routes)):
                rt2: Route = self.sol.routes[secondRouteIndex]
                for firstNodeIndex in range(1, len(rt1.sequenceOfNodes)):
                    startOfSecondNodeIndex = 1
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range(startOfSecondNodeIndex, len(rt2.sequenceOfNodes)):

                        A = rt1.sequenceOfNodes[firstNodeIndex - 1]
                        B = rt1.sequenceOfNodes[firstNodeIndex]

                        if (rt1.sequenceOfNodes[firstNodeIndex] == rt1.sequenceOfNodes[-1]):
                            C = rt1.sequenceOfNodes[firstNodeIndex]
                        else:
                            C = rt1.sequenceOfNodes[firstNodeIndex + 1]

                        E = rt2.sequenceOfNodes[secondNodeIndex - 1]
                        F = rt2.sequenceOfNodes[secondNodeIndex]

                        if (rt2.sequenceOfNodes[secondNodeIndex] == rt2.sequenceOfNodes[-1]):
                            G = rt2.sequenceOfNodes[secondNodeIndex]
                        else:
                            G = rt2.sequenceOfNodes[secondNodeIndex + 1]

                        moveCost = 0

                        originRtCostChange = 0
                        targetRtCostChange = 0
                        originRtTimeChange = 0
                        targetRtTimeChange = 0

                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
                                costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][F.ID] + \
                                              self.distanceMatrix[F.ID][G.ID]
                                costAdded = self.distanceMatrix[A.ID][F.ID] + self.distanceMatrix[F.ID][B.ID] + \
                                            self.distanceMatrix[B.ID][G.ID]
                                moveCost = costAdded - costRemoved
                                originRtCostChange = costAdded - costRemoved

                                originRtTimeChange = self.timeMatrix[A.ID][F.ID] + self.timeMatrix[F.ID][B.ID] + \
                                                     self.timeMatrix[B.ID][G.ID] - self.distanceMatrix[A.ID][B.ID] \
                                                     - self.distanceMatrix[B.ID][F.ID] - self.distanceMatrix[F.ID][G.ID]

                                if (rt1.sequenceOfNodes[secondNodeIndex] == rt1.sequenceOfNodes[-1]):
                                    costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][F.ID]
                                    costAdded = self.distanceMatrix[A.ID][F.ID] + self.distanceMatrix[F.ID][B.ID]
                                    moveCost = costAdded - costRemoved
                                    originRtCostChange = costAdded - costRemoved
                                    originRtTimeChange = self.timeMatrix[A.ID][F.ID] + self.timeMatrix[F.ID][B.ID] - \
                                                         self.distanceMatrix[A.ID][B.ID] - self.distanceMatrix[B.ID][
                                                             F.ID]

                            else:

                                costRemoved1 = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID]
                                costAdded1 = self.distanceMatrix[A.ID][F.ID] + self.distanceMatrix[F.ID][C.ID]
                                costRemoved2 = self.distanceMatrix[E.ID][F.ID] + self.distanceMatrix[F.ID][G.ID]
                                costAdded2 = self.distanceMatrix[E.ID][B.ID] + self.distanceMatrix[B.ID][G.ID]
                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)

                                originRtCostChange = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                                originRtTimeChange = self.timeMatrix[A.ID][F.ID] + self.timeMatrix[F.ID][C.ID] - \
                                                     self.timeMatrix[A.ID][B.ID] - self.timeMatrix[B.ID][C.ID] + \
                                                     self.timeMatrix[E.ID][B.ID] + self.timeMatrix[B.ID][G.ID] - \
                                                     self.timeMatrix[E.ID][F.ID] - self.timeMatrix[F.ID][G.ID]

                                if (rt1.sequenceOfNodes[secondNodeIndex] == rt1.sequenceOfNodes[-1]):
                                    costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID] + \
                                                  self.distanceMatrix[E.ID][F.ID]
                                    costAdded = self.distanceMatrix[A.ID][F.ID] + self.distanceMatrix[F.ID][C.ID] + \
                                                self.distanceMatrix[E.ID][B.ID]
                                    moveCost = costAdded - costRemoved
                                    originRtCostChange = costAdded - costRemoved

                                    originRtTimeChange = self.timeMatrix[A.ID][F.ID] + self.timeMatrix[F.ID][C.ID] + \
                                                         self.timeMatrix[E.ID][B.ID] - self.timeMatrix[A.ID][B.ID] - \
                                                         self.timeMatrix[B.ID][C.ID] - self.timeMatrix[E.ID][F.ID]

                        else:

                            costRemoved1 = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID]
                            costAdded1 = self.distanceMatrix[A.ID][F.ID] + self.distanceMatrix[F.ID][C.ID]
                            costRemoved2 = self.distanceMatrix[E.ID][F.ID] + self.distanceMatrix[F.ID][G.ID]
                            costAdded2 = self.distanceMatrix[E.ID][B.ID] + self.distanceMatrix[B.ID][G.ID]

                            originRtCostChange = costAdded1 - costRemoved1
                            targetRtCostChange = costAdded2 - costRemoved2
                            originRtTimeChange = self.timeMatrix[A.ID][F.ID] + self.timeMatrix[F.ID][C.ID] - \
                                                 self.timeMatrix[A.ID][B.ID] - self.timeMatrix[B.ID][C.ID]
                            targetRtTimeChange = self.timeMatrix[E.ID][B.ID] + self.timeMatrix[B.ID][G.ID] - \
                                                 self.timeMatrix[E.ID][F.ID] - self.timeMatrix[F.ID][G.ID]

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)

                            if (rt2.sequenceOfNodes[secondNodeIndex] == rt2.sequenceOfNodes[-1]):
                                costRemoved1 = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID]
                                costAdded1 = self.distanceMatrix[A.ID][F.ID] + self.distanceMatrix[F.ID][C.ID]
                                costRemoved2 = self.distanceMatrix[E.ID][F.ID]
                                costAdded2 = self.distanceMatrix[E.ID][B.ID]

                                originRtCostChange = costAdded1 - costRemoved1
                                targetRtCostChange = costAdded2 - costRemoved2
                                originRtTimeChange = self.timeMatrix[A.ID][F.ID] + self.timeMatrix[F.ID][C.ID] - \
                                                     self.timeMatrix[A.ID][B.ID] - self.timeMatrix[B.ID][C.ID]
                                targetRtTimeChange = self.timeMatrix[E.ID][B.ID] - self.timeMatrix[E.ID][F.ID]

                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)

                            if (rt1.sequenceOfNodes[firstNodeIndex] == rt1.sequenceOfNodes[-1]):
                                if (rt2.sequenceOfNodes[secondNodeIndex] == rt2.sequenceOfNodes[-1]):

                                    costRemoved1 = self.distanceMatrix[A.ID][B.ID]
                                    costAdded1 = self.distanceMatrix[A.ID][F.ID]
                                    costRemoved2 = self.distanceMatrix[E.ID][F.ID]
                                    costAdded2 = self.distanceMatrix[E.ID][B.ID]

                                    originRtCostChange = costAdded1 - costRemoved1
                                    targetRtCostChange = costAdded2 - costRemoved2
                                    originRtTimeChange = self.timeMatrix[A.ID][F.ID] - self.timeMatrix[A.ID][B.ID]
                                    targetRtTimeChange = self.timeMatrix[E.ID][B.ID] - self.timeMatrix[E.ID][F.ID]

                                    moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                                else:
                                    costRemoved1 = self.distanceMatrix[A.ID][B.ID]
                                    costAdded1 = self.distanceMatrix[A.ID][F.ID]
                                    costRemoved2 = self.distanceMatrix[E.ID][F.ID] + self.distanceMatrix[F.ID][G.ID]
                                    costAdded2 = self.distanceMatrix[E.ID][B.ID] + self.distanceMatrix[B.ID][G.ID]

                                    originRtCostChange = costAdded1 - costRemoved1
                                    targetRtCostChange = costAdded2 - costRemoved2
                                    originRtTimeChange = self.timeMatrix[A.ID][F.ID] - self.timeMatrix[A.ID][B.ID]
                                    targetRtTimeChange = self.timeMatrix[E.ID][B.ID] + self.timeMatrix[B.ID][G.ID] - \
                                                         self.distanceMatrix[E.ID][F.ID] - self.distanceMatrix[F.ID][
                                                             G.ID]

                                    moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)

                        if rt1 == rt2:
                            if rt1.time + originRtTimeChange + targetRtTimeChange > 3.5:
                                continue
                        if rt1 != rt2:
                            if rt1.load - B.demand + F.demand > rt1.capacity:
                                continue
                            if rt2.load - F.demand + B.demand > rt2.capacity:
                                continue
                            if rt1.time + originRtTimeChange > 3.5:
                                continue
                            if rt2.time + targetRtTimeChange > 3.5:
                                continue

                        if moveCost < sm.moveCost and abs(moveCost) > 0.0001:
                            self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex,
                                                   moveCost, originRtCostChange, targetRtCostChange, originRtTimeChange,
                                                   targetRtTimeChange, sm)

    def StoreBestSwapMove(self, firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost,
                          originRtCostChange, targetRtCostChange, originRtTimeChange, targetRtTimeChange, sm):
        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.originRtCostChange = originRtCostChange
        sm.targetRtCostChange = targetRtCostChange
        sm.originRtTimeChange = originRtTimeChange
        sm.targetRtTimeChange = targetRtTimeChange
        sm.moveCost = moveCost

    def ApplySwapMove(self, sm):
        oldCost = self.objective(self.sol)
        rt1 = self.sol.routes[sm.positionOfFirstRoute]
        rt2 = self.sol.routes[sm.positionOfSecondRoute]
        b1 = rt1.sequenceOfNodes[sm.positionOfFirstNode]
        b2 = rt2.sequenceOfNodes[sm.positionOfSecondNode]
        rt1.sequenceOfNodes[sm.positionOfFirstNode] = b2
        rt2.sequenceOfNodes[sm.positionOfSecondNode] = b1

        if (rt1 == rt2):
            rt1.distance += sm.moveCost
            rt1.time += sm.originRtTimeChange
            rt1.time += sm.targetRtTimeChange
        else:
            rt1.distance += sm.originRtCostChange
            rt2.distance += sm.targetRtCostChange
            rt1.load = rt1.load - b1.demand + b2.demand
            rt2.load = rt2.load + b1.demand - b2.demand
            rt1.time += sm.originRtTimeChange
            rt2.time += sm.targetRtTimeChange

        self.sol.cost += sm.moveCost

        #This is an alternative way of checking the solution.
        # newCost = self.objective(self.sol)
        # print(newCost, oldCost, sm.moveCost)
        # # debuggingOnly
        # if abs((newCost - oldCost) - sm.moveCost) > 0.0001:
        #     print('Cost Issue')
        self.TestSolution()


    def FindBestTwoOptMove(self, top):
        for rtInd1 in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[rtInd1]
            for rtInd2 in range(rtInd1, len(self.sol.routes)):
                rt2: Route = self.sol.routes[rtInd2]
                for nodeInd1 in range(0, len(rt1.sequenceOfNodes)):  # -1 to 0
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2

                    for nodeInd2 in range(start2, len(rt2.sequenceOfNodes)):  # -1 to 0
                        moveCost = 10 ** 9

                        A = rt1.sequenceOfNodes[nodeInd1]
                        if (rt1.sequenceOfNodes[nodeInd1] == rt1.sequenceOfNodes[-1]):
                            B = rt1.sequenceOfNodes[nodeInd1]
                        else:
                            B = rt1.sequenceOfNodes[nodeInd1 + 1]

                        K = rt2.sequenceOfNodes[nodeInd2]
                        if (rt2.sequenceOfNodes[nodeInd2] == rt2.sequenceOfNodes[-1]):
                            L = rt2.sequenceOfNodes[nodeInd2]
                        else:
                            L = rt2.sequenceOfNodes[nodeInd2 + 1]

                        originRtCostChange = 0
                        targetRtCostChange = 0
                        originRtTimeChange = 0
                        targetRtTimeChange = 0

                        if rt1 == rt2:
                            if nodeInd1 == 0 and nodeInd2 == len(rt1.sequenceOfNodes) - 1:  # -2 to -1
                                continue
                            costAdded = self.distanceMatrix[A.ID][K.ID] + self.distanceMatrix[B.ID][L.ID]
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[K.ID][L.ID]
                            moveCost = costAdded - costRemoved

                            originRtCostChange = costAdded - costRemoved
                            originRtTimeChange = self.timeMatrix[A.ID][K.ID] + self.timeMatrix[B.ID][L.ID] - \
                                                 self.timeMatrix[A.ID][B.ID] - self.timeMatrix[K.ID][L.ID]

                            if rt1.time + originRtTimeChange > 3.5:
                                continue
                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue
                            if nodeInd1 == len(rt1.sequenceOfNodes) - 1 and nodeInd2 == len(
                                    rt2.sequenceOfNodes) - 1:  # -2 to -1
                                continue

                            if self.CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
                                continue

                            originRtCostChange = 0
                            originRtTimeChange = 0

                            #calculating the time of rt1
                            for i in range(0, nodeInd1):  # time from 0 to A in rt1
                                index1 = rt1.sequenceOfNodes[i]
                                index2 = rt1.sequenceOfNodes[i + 1]
                                originRtCostChange += self.distanceMatrix[index1.ID][index2.ID]
                                originRtTimeChange += self.timeMatrix[index1.ID][index2.ID]

                            originRtCostChange += self.distanceMatrix[A.ID][L.ID]
                            originRtTimeChange += self.timeMatrix[A.ID][L.ID]  # time from A to L in rt1

                            for i in range(nodeInd2 + 1, len(rt2.sequenceOfNodes) - 1):  # time from L to end in rt2
                                index1 = rt2.sequenceOfNodes[i]
                                index2 = rt2.sequenceOfNodes[i + 1]
                                originRtCostChange += self.distanceMatrix[index1.ID][index2.ID]
                                originRtTimeChange += self.timeMatrix[index1.ID][index2.ID]

                            if originRtTimeChange > 3.5:
                                continue

                            #Calculating the time of rt2
                            targetRtCostChange = 0
                            targetRtTimeChange = 0
                            for i in range(0, nodeInd2):  # time from 0 to K in rt2
                                index1 = rt2.sequenceOfNodes[i]
                                index2 = rt2.sequenceOfNodes[i + 1]
                                targetRtCostChange += self.distanceMatrix[index1.ID][index2.ID]
                                targetRtTimeChange += self.timeMatrix[index1.ID][index2.ID]
                            targetRtCostChange += self.distanceMatrix[K.ID][B.ID]  # time from K to B in rt2
                            targetRtTimeChange += self.timeMatrix[K.ID][B.ID]  # time from K to B in rt2

                            for i in range(nodeInd1 + 1, len(rt1.sequenceOfNodes) - 1):  # time from B to end in rt1
                                index1 = rt1.sequenceOfNodes[i]
                                index2 = rt1.sequenceOfNodes[i + 1]
                                targetRtCostChange += self.distanceMatrix[index1.ID][index2.ID]
                                targetRtTimeChange += self.timeMatrix[index1.ID][index2.ID]

                            if targetRtTimeChange > 3.5:
                                continue

                            costAdded = self.distanceMatrix[A.ID][L.ID] + self.distanceMatrix[B.ID][K.ID]
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[K.ID][L.ID]
                            moveCost = costAdded - costRemoved

                        if moveCost < top.moveCost and abs(moveCost) > 0.0001:
                            self.StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, originRtCostChange,
                                                     targetRtCostChange, originRtTimeChange, targetRtTimeChange,
                                                     top)

    def CapacityIsViolated(self, rt1, nodeInd1, rt2, nodeInd2):

        rt1FirstSegmentLoad = 0
        for i in range(0, nodeInd1 + 1):
            n = rt1.sequenceOfNodes[i]
            rt1FirstSegmentLoad += n.demand
        rt1SecondSegmentLoad = rt1.load - rt1FirstSegmentLoad

        rt2FirstSegmentLoad = 0
        for i in range(0, nodeInd2 + 1):
            n = rt2.sequenceOfNodes[i]
            rt2FirstSegmentLoad += n.demand
        rt2SecondSegmentLoad = rt2.load - rt2FirstSegmentLoad

        if (rt1FirstSegmentLoad + rt2SecondSegmentLoad > rt1.capacity):
            return True
        if (rt2FirstSegmentLoad + rt1SecondSegmentLoad > rt2.capacity):
            return True

        return False

    def StoreBestTwoOptMove(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost,
                            originRtCostChange, targetRtCostChange, originRtTimeChange, targetRtTimeChange, top):
        top.positionOfFirstRoute = rtInd1
        top.positionOfSecondRoute = rtInd2
        top.positionOfFirstNode = nodeInd1
        top.positionOfSecondNode = nodeInd2
        top.moveCost = moveCost
        top.originRtCostChange = originRtCostChange
        top.targetRtCostChange = targetRtCostChange
        top.originRtTimeChange = originRtTimeChange
        top.targetRtTimeChange = targetRtTimeChange

    def ApplyTwoOptMove(self, top):
        oldCost = self.objective(self.sol)
        rt1: Route = self.sol.routes[top.positionOfFirstRoute]
        rt2: Route = self.sol.routes[top.positionOfSecondRoute]

        if rt1 == rt2:
            # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
            reversedSegment = reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            # lst = list(reversedSegment)
            # lst2 = list(reversedSegment)
            rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegment

            # reversedSegmentList = list(reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1]))
            # rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegmentList

            rt1.distance += top.moveCost

        else:
            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt1 = rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]

            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt2 = rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            del rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]
            del rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            rt1.sequenceOfNodes.extend(relocatedSegmentOfRt2)
            rt2.sequenceOfNodes.extend(relocatedSegmentOfRt1)

            self.UpdateRouteCostAndLoadAndTime(rt1)
            self.UpdateRouteCostAndLoadAndTime(rt2)

        self.sol.cost += top.moveCost

        # This is an alternative way of checking the solution.
        # newCost = self.objective(self.sol)
        # print(newCost, oldCost, top.moveCost)
        # # debuggingOnly
        # if abs((newCost - oldCost) - top.moveCost) > 0.0001:
        #     print('Cost Issue')

        self.TestSolution()

    def UpdateRouteCostAndLoadAndTime(self, rt: Route):
        tc = 0
        tl = 0
        tt = 0
        for i in range(0, len(rt.sequenceOfNodes) - 1):
            A = rt.sequenceOfNodes[i]
            B = rt.sequenceOfNodes[i + 1]
            tc += self.distanceMatrix[A.ID][B.ID]
            tt += self.timeMatrix[A.ID][B.ID]
            tl += A.demand
        rt.load = tl
        lastNodeOfRoute = rt.sequenceOfNodes[-1]
        rt.load += lastNodeOfRoute.demand

        rt.time = tt
        rt.distance = tc

    def TestSolution(self):
        totalSolCost = 0
        for r in range(0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            rtCost = 0
            rtLoad = 0
            for n in range(0, len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[n]
                B = rt.sequenceOfNodes[n + 1]
                rtCost += self.distanceMatrix[A.ID][B.ID]
                rtLoad += A.demand
            lastNodeOfRoute = rt.sequenceOfNodes[-1]
            rtLoad += lastNodeOfRoute.demand
            if abs(rtCost - rt.distance) > 0.0001:
                print('Route Cost problem')
            if rtLoad != rt.load:
                print('Route Load problem')

            totalSolCost += rt.distance

        if abs(totalSolCost - self.objective(self.sol)) > 0.0001:
            print('Solution Cost problem')
            print(totalSolCost)
            print(self.sol.cost)
