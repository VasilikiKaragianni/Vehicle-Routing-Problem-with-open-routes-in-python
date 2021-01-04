from BESTFIT import Model
from BESTFIT import Route
from BESTFIT import Node


class Solution:
    def __init__(self):
        self.all_routes = [] #All best-fit routes
        self.allTime = 0
        self.allDist = 0
        self.cost = 0.0
        self.sequenceOfTSPNodes = [] #All tsp sequences

def SetRoutedFlagToFalseForAllCustomers(customers):
    for i in range (0, len(customers)):
        customers[i].isRouted = False


def ApplyNearestNeighborMethod(depot, customers, sol, distanceMatrix):
    sol.sequenceOfTSPNodes.append(depot)
    for i in range (0, len(customers)):
        indexOfTheNextCustomer = -1
        minimumInsertionCost = 1000000
        lastIndexInSolution = len(sol.sequenceOfTSPNodes) - 1
        lastNodeInTheCurrentSequence = sol.sequenceOfTSPNodes[lastIndexInSolution]

        for j in range (0, len(customers)):
            candidate = customers[j]
            if candidate.isRouted == True:
                continue
            trialCost = distanceMatrix[lastNodeInTheCurrentSequence.id][candidate.id]
            if (trialCost < minimumInsertionCost):
                indexOfTheNextCustomer = j
                minimumInsertionCost = trialCost

        insertedCustomer = customers[indexOfTheNextCustomer]
        sol.sequenceOfTSPNodes.append(insertedCustomer)
        sol.cost += distanceMatrix[lastNodeInTheCurrentSequence.id][insertedCustomer.id]
        insertedCustomer.isRouted = True

    lastIndexInSolution = len(sol.sequenceOfTSPNodes) - 1
    lastNodeInTheCurrentSequence = sol.sequenceOfTSPNodes[lastIndexInSolution]
    sol.sequenceOfTSPNodes.append(depot)
    sol.cost += distanceMatrix[lastNodeInTheCurrentSequence.id][depot.id]



def ReportSolution(sol):
    for i in range (0, len(sol.sequenceOfTSPNodes)):
        print(sol.sequenceOfTSPNodes[i].id, end = ' ')


def CheckSolution(sol, distanceMatrix):
    cst = 0
    for i in range(len(sol.sequenceOfTSPNodes) - 1):
        a = sol.sequenceOfTSPNodes[i]
        b = sol.sequenceOfTSPNodes[i+1]
        cst += distanceMatrix[a.id][b.id]
    if (abs(cst - sol.cost) > 0.00001):
        print('Error')

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


def solve(m):
    allNodes = m.allNodes
    allTime = m.time
    allDist = m.distance
    sol = Solution()
    capacity = 1500
    all_nodes = allNodes

    BestFit(sol, all_nodes, capacity)
    all_TSP_Nodes = m.allNodes
    customers = m.customers
    depot = all_TSP_Nodes[0]
    distanceMatrix = m.distance

    for i in range(0,len(sol.all_routes)):
        #print(len(sol.all_routes))
        customers = sol.all_routes[i].sequenceOfNodes
        print(customers)
        ApplyNearestNeighborMethod(depot, customers, sol, distanceMatrix)
        CheckSolution(sol, distanceMatrix)
        ReportSolution(sol)


m = Model()
m.BuildModel()
solve(m)