import random
import math

class Model:

# instance variables
    def __init__(self):
        self.allNodes = []
        self.customers = []
        self.distance = []
        self.time = []
        self.capacity = -1
        self.numberOf1500 = 15
        self.numberOf1200 = 15

    def BuildModel(self):
        # birthday 08/02/1999
        birthday = 8021999
        random.seed(birthday)
        self.allNodes = []
        self.customers = []
        depot = Node(0, 0, 0, 50, 50)
        self.allNodes.append(depot)
        random.seed(1)
        for i in range(0, 100):
            id = i + 1
            dem = random.randint(1, 5) * 100
            xx = random.randint(0, 100)
            yy = random.randint(0, 100)
            st = 0.25  # 15 minutes in hrs
            cust = Node(id, st, dem, xx, yy)
            self.allNodes.append(cust)
            self.customers.append(cust)

            rows = len(self.allNodes)
            self.distance = [[0.0 for x in range(rows)] for y in range(rows)]
            self.time = [[0.0 for x in range(rows)] for y in range(rows)]

            for i in range(0, len(self.allNodes)):
                for j in range(0, len(self.allNodes)):
                    a = self.allNodes[i]
                    b = self.allNodes[j]
                    dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                    self.distance[i][j] = dist
                    self.time[i][j] = dist / 35 + 0.25


class Node:
    def __init__(self, id, st, dem, xx, yy):
        self.id = id
        self.service_time = st
        self.demand = dem
        self.x = xx
        self.y = yy
        self.isRouted = False

class Route:
    def __init__(self, cap):
        self.sequenceOfNodes = []
        self.capacity = cap
        self.load = 0
        self.maxtime = 3.5
        self.time = 0
        self.distance = 0

class Solution:
    def __init__(self):
        self.all_routes = []
        self.allTime = 0
        self.allDist = 0

def BestFit(sol, all_nodes, capacity):
    #sol.all_routes.append(all_nodes)
    totalNodes = len(all_nodes)
    counter = 0
    for i in range(0, totalNodes):

        toBeAssigned = all_nodes[i]
        indexOfBestRoutes = -1
        minimumEmptySpace = 1000000

        totalRoutes = len(sol.all_routes)
        for b in range(0, totalRoutes):
            trialRoute = sol.all_routes[b]
            if (capacity - trialRoute.load >= toBeAssigned.demand):
                if (capacity - trialRoute.load < minimumEmptySpace):
                    if(len(trialRoute.sequenceOfNodes)>0):
                        last_cust = trialRoute.sequenceOfNodes[-1]
                        last_id = last_cust.id
                        current_id = toBeAssigned.id



                    minimumEmptySpace = capacity - trialRoute.load
                    indexOfBestRoutes = b

        if (indexOfBestRoutes != -1):

            route_Of_Insertion: Route = sol.all_routes[indexOfBestRoutes]
            route_Of_Insertion.sequenceOfNodes.append(toBeAssigned)
            route_Of_Insertion.load = route_Of_Insertion.load + toBeAssigned.demand
            toBeAssigned.isRouted = True
            counter+=1

        else:
            m.numberOf1500 = m.numberOf1500 - 1
            if (m.numberOf1500>0):

                capacity = 1500
                newRoute = Route(capacity)
                newRoute.capacity = capacity
                newRoute.load = 0
                sol.all_routes.append(newRoute)
                newRoute.sequenceOfNodes.append(toBeAssigned)
                newRoute.load = newRoute.load + toBeAssigned.demand
                toBeAssigned.isRouted = True
                counter += 1
            else:
                m.numberOf1200 = m.numberOf1200 - 1
                if(m.numberOf1200>0):
                    busCapacity2 = 1200
                    newRoute = Route(capacity)
                    newRoute.capacity = capacity
                    newRoute.load = 0
                    sol.all_routes.append(newRoute)
                    newRoute.sequenceOfNodes.append(toBeAssigned)
                    newRoute.load = newRoute.load + toBeAssigned.demand
                    toBeAssigned.isRouted = True
                    counter += 1
                else:
                    print("There are not buses to complete the route ")
    print("counter is")
    print(counter)

def solve(m):

    allNodes = m.allNodes
    allTime = m.time
    allDist = m.distance
    sol = Solution()
    capacity = 1500
    all_nodes = allNodes

    BestFit(sol, all_nodes, capacity)

    print(len(sol.all_routes))
    sol.all_routes.clear()

m = Model()
m.BuildModel()
solve(m)