from VRP_Model import *
from SolutionDrawer import *


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

class Solver:
    def __init__(self,m):
        self.allNodes = m.allNodes
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.distance
        self.timeMatrix = m.time
        self.capacity = m.capacity
        self.solution_list = []
        self.time_list = []
        self.sol = Solution()
        self.route = None

    def ApplyNearestNeighborMethod(self):

        isRouted = []
        for i in range(len(self.allNodes)):
            isRouted.append(False)

        for t in range(30):
            capacity = 1500
            if t > 14:
                capacity = 1200
                self.route = Route(1200)
            else:
                self.route = Route(1500)
            solution = []
            node = 0
            self.route.sequenceOfNodes.append(self.allNodes[0])
            self.allNodes[0].isRouted = True
            solution.append(node)
            isRouted[0] = True
            total_demand = 0
            total_time = 0
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
                elif total_demand + self.allNodes[position].demand <= capacity and total_time + self.timeMatrix[node][position] <= 3.5:
                    # print(position)
                    solution.append(position)                                     #katia's way
                    isRouted[position] = True                                     #katia's way
                    self.route.sequenceOfNodes.append(self.allNodes[position])   ##zahariadi's way
                    self.allNodes[position].isRouted = True                      ##zahariadi's way
                    a = self.allNodes[position]
                    total_demand += a.demand
                    total_time += self.timeMatrix[node][position]
                    node = position
                else:
                    break
            print(solution)
            print(total_demand)
            self.route.load = total_demand
            self.route.capacity = capacity
            self.route.time = total_time
            self.solution_list.append(solution)
            self.sol.routes.append(self.route)
            self.time_list.append(total_time)
            SolDrawer.draw(t,self.sol,self.allNodes)

        print(self.solution_list)
        print(self.time_list)
        print(isRouted)
        return (self.sol)

 ## method that calculates the total cost of the solution given
    def objective (self,solution):
        total_cost = 0
        single_cost = []
        for i in range(len(solution.routes)):
            cost = 0
            rout :Route = solution.routes[i]
            for j in range(len(rout.sequenceOfNodes) - 1):
                index1 = rout.sequenceOfNodes[j]
                index2 = rout.sequenceOfNodes[j + 1]
                cost += self.distanceMatrix[index1.ID][index2.ID]
            single_cost.append(cost)
            self.sol.routes[i].cost = cost
            total_cost += cost
        return total_cost


    def LocalSearch(self):
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        counter = 0
        rm = RelocationMove()
        localSearchIterator = 0
        while terminationCondition is False:

            SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)
            self.InitializeOperators(rm)
            # Relocations
            # if operator == 0:
            self.FindBestRelocationMove(rm)
            if rm.originRoutePosition is not None:
                if rm.moveCost < 0:
                    self.ApplyRelocationMove(rm)
                    counter += 1
                else:
                    terminationCondition = True
            localSearchIterator += 1
        # print(counter)
        for i in range(len(self.sol.routes)):
            rt:Route = self.sol.routes[i]
            print(rt.capacity)
            print(rt.load)
            print(rt.time)
            for j in range(len(rt.sequenceOfNodes)):
                print(rt.sequenceOfNodes[j].ID, end=' ',)
                # print(rt.sequenceOfNodes[j].isRouted)
            print("\n")
        print("hiiiiiiiiiiiiiiiiiiiiiiiii")
        print(self.timeMatrix[0][53]+self.timeMatrix[53][37]+self.timeMatrix[37][96])
        print(self.timeMatrix[0][46])
        print(self.timeMatrix[0][3] + self.timeMatrix[3][23] + self.timeMatrix[23][8])
        print(self.timeMatrix[0][72] + self.timeMatrix[72][31] + self.timeMatrix[31][2]+ self.timeMatrix[2][91] + self.timeMatrix[91][51])

        # print(len(self.sol.routes))

    def cloneRoute(self, rt: Route):
        cloned = Route(self.capacity)
        cloned.cost = rt.cost
        cloned.load = rt.load
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
                            break
                        else:
                            C = rt1.sequenceOfNodes[originNodeIndex + 1]

                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        if (rt2.sequenceOfNodes[targetNodeIndex] == rt2.sequenceOfNodes[-1]):
                            break
                        else:
                            G = rt2.sequenceOfNodes[targetNodeIndex + 1]

                        if rt1 != rt2:
                            if rt2.load + B.demand > rt2.capacity:
                                continue

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
                                                         targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange,
                                                         originRtTimeChange, targetRtTimeChange,rm)

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
            originRt.cost += rm.moveCost
        else:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt.cost += rm.costChangeOriginRt
            targetRt.cost += rm.costChangeTargetRt
            originRt.load -= B.demand
            targetRt.load += B.demand
            originRt.time += rm.originRtTimeChange
            targetRt.time += rm.targetRtTimeChange

        self.sol.cost += rm.moveCost

        newCost = self.objective(self.sol)
        print(newCost,oldCost,rm.moveCost)
        # debuggingOnly
        if abs((newCost - oldCost) - rm.moveCost) > 0.0001:
            print('Cost Issue')

    def InitializeOperators(self, rm):
        rm.Initialize()

    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, originRtTimeChange, targetRtTimeChange,  rm:RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost
        rm.originRtTimeChange = originRtTimeChange
        rm.targetRtTimeChange = targetRtTimeChange