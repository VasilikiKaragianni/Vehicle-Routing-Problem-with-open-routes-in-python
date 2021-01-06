from VRP_Model import *
from SolutionDrawer import *


class Solution:
    def __init__(self):
        self.cost = 0
        self.routes = []

class Solver:
    def __init__(self,m):
        self.allNodes = m.allNodes
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.distance
        self.timeMatrix = m.time
        # self.capacity = m.capacity
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
            self.solution_list.append(solution)
            self.sol.routes.append(self.route)
            self.time_list.append(total_time)
            SolDrawer.draw(t,self.sol,self.allNodes)

        print(self.solution_list)
        print(self.time_list)
        print(isRouted)

 ## method that calculates the total cost of the solution given
    def objective (self):
        total_cost = 0
        single_cost = []
        for i in range(len(self.solution_list)):
            cost = 0
            for j in range(len(self.solution_list[i]) - 1):
                index1 = self.solution_list[i][j]
                index2 = self.solution_list[i][j + 1]
                cost += self.distanceMatrix[index1][index2]
            single_cost.append(cost)
            total_cost += cost
        return total_cost