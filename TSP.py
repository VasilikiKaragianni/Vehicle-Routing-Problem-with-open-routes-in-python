from VRP_Model import *


class Solution:
    all_routes = []  # All best-fit routes
    allTime = 0
    allDist = 0
    # cost = 0.0
    # sequenceOfTSPNodes = []  # All tsp sequences

    # def __init__(self):


def SetRoutedFlagToFalseForAllCustomers(customers):
    for i in range(0, len(customers)):
        customers[i].isRouted = False


def ApplyNearestNeighborMethod(depot, customers, sol, distanceMatrix, timeMatrix):
    sequenceOfTSPNodes = []
    distance = 0
    time = 0
    sequenceOfTSPNodes.append(customers[0])

    for i in range(1, len(customers)):
        indexOfTheNextCustomer = -1
        minimumInsertionCost = 1000000
        # lastIndexInSolution = len(sequenceOfTSPNodes) - 1
        lastNodeInTheCurrentSequence = sequenceOfTSPNodes[-1]

        for j in range(1, len(customers)):
            candidate = customers[j]
            if candidate in sequenceOfTSPNodes:
                continue
            trialCost = distanceMatrix[lastNodeInTheCurrentSequence.id][candidate.id]
            if (trialCost < minimumInsertionCost):
                indexOfTheNextCustomer = j
                minimumInsertionCost = trialCost

        insertedCustomer = customers[indexOfTheNextCustomer]
        sequenceOfTSPNodes.append(insertedCustomer)
        distance += distanceMatrix[lastNodeInTheCurrentSequence.id][insertedCustomer.id]
        time += timeMatrix[lastNodeInTheCurrentSequence.id][insertedCustomer.id]
        insertedCustomer.isRouted = True

    for j in sequenceOfTSPNodes:
        print(j.id, end=' ')
    print()
    return sequenceOfTSPNodes, distance, time


def ReportSolution(customersOfRoute):
    for i in customersOfRoute:
        print(i.id, end=' ')


def CheckSolution(customersOfRoute, dist, distanceMatrix):
    cst = 0
    for i in range(len(customersOfRoute) - 1):
        a = customersOfRoute[i]
        b = customersOfRoute[i + 1]
        cst += distanceMatrix[a.id][b.id]
    if (abs(cst - dist) > 0.00001):
        print('Error')


def BestFit(sol, all_nodes, timeMatrix, distanceMatrix):
    # sol.all_routes.append(all_nodes)
    # totalNodes = len(all_nodes)

    all_nodes.sort(key=lambda x: x.demand)
    counter = 0
    for i in range(0, len(all_nodes)):

        toBeAssigned = all_nodes[i]

        indexOfBestRoutes = -1
        minimumEmptySpace = 1000000

        # totalRoutes = len(sol.all_routes)
        for b in range(0, len(sol.all_routes)):
            trialRoute = sol.all_routes[b]
            if (trialRoute.capacity - trialRoute.load >= toBeAssigned.demand):

                lastcust = trialRoute.sequenceOfNodes[-1]
                i = toBeAssigned.id
                j = lastcust.id

                if (trialRoute.capacity - trialRoute.load < minimumEmptySpace):
                    minimumEmptySpace = trialRoute.capacity - trialRoute.load
                    indexOfBestRoutes = b
                    timeAdded = timeMatrix[j][i]
                    distanceAdded = distanceMatrix[j][i]

        if (indexOfBestRoutes != -1):

            route_Of_Insertion: Route = sol.all_routes[indexOfBestRoutes]
            route_Of_Insertion.sequenceOfNodes.append(toBeAssigned)
            route_Of_Insertion.load += toBeAssigned.demand
            toBeAssigned.isRouted = True

            counter += 1

            route_Of_Insertion.time += timeAdded
            route_Of_Insertion.distance += distanceAdded



        else:

            if (m.numberOf1500 > 0):
                m.numberOf1500 -= 1

                newRoute = Route(1500)
                sol.all_routes.append(newRoute)
                depot = Node(0, 0, 0, 50, 50)
                newRoute.sequenceOfNodes.append(depot)

                newRoute.sequenceOfNodes.append(toBeAssigned)
                newRoute.load += toBeAssigned.demand
                toBeAssigned.isRouted = True
                counter += 1

                lastcust = newRoute.sequenceOfNodes[-1]
                i = toBeAssigned.id
                j = lastcust.id
                timeAdded = timeMatrix[j][i]
                distanceAdded = distanceMatrix[j][i]
                newRoute.time += timeAdded
                newRoute.distance += distanceAdded

            else:

                if (m.numberOf1200 > 0):
                    m.numberOf1200 -= 1

                    newRoute = Route(1200)
                    sol.all_routes.append(newRoute)
                    depot = Node(0, 0, 0, 50, 50)
                    newRoute.sequenceOfNodes.append(depot)

                    newRoute.sequenceOfNodes.append(toBeAssigned)
                    newRoute.load += toBeAssigned.demand
                    toBeAssigned.isRouted = True
                    counter += 1

                    lastcust = newRoute.sequenceOfNodes[-1]
                    i = toBeAssigned.id
                    j = lastcust.id
                    timeAdded = timeMatrix[j][i]
                    distanceAdded = distanceMatrix[j][i]
                    newRoute.time += timeAdded
                    newRoute.distance += distanceAdded

                else:
                    print("There are not buses to complete the route ")


def solve(m):
    all_Nodes = m.allNodes
    timeMatrix = m.time
    distanceMatrix = m.distance
    sol = Solution()
    # all_nodes = allNodes
    customers = m.customers

    BestFit(sol, customers, timeMatrix, distanceMatrix)
    # all_TSP_Nodes = m.allNodes

    depot = m.allNodes[0]
    # print(depot.id,
    #       depot.service_time,
    #       depot.demand,
    #       depot.x,
    #       depot.y,
    #       depot.isRouted)
    #
    for i in sol.all_routes:
        print(i.load, i.time, i.distance)
        for j in i.sequenceOfNodes:
            print(j.id, end=' ')
        print()

    print(len(sol.all_routes))

    for i in sol.all_routes:
        customersOfRoute = i.sequenceOfNodes
        # print(customers)
        i.sequenceOfNodes, i.distance, i.time = ApplyNearestNeighborMethod(depot, customersOfRoute, sol, distanceMatrix,
                                                                           timeMatrix)

        CheckSolution(i.sequenceOfNodes, i.distance, distanceMatrix)
        print(i.load, i.time, i.distance)
        ReportSolution(customersOfRoute)

        print()

    counter = 0
    # for i in sol.all_routes:
    #     if i.time > 3.5:
    #         counter += 1
    #         print(i.load, i.time, i.distance)
    # print(counter)
    # ApplyNearestNeighborMethod(depot, customers, sol, distanceMatrix)
    # # MinimumInsertions(depot, customers, sol, distanceMatrix)
    # CheckSolution(sol, distanceMatrix)
    # ReportSolution(sol)
    # SolDrawer.draw(0, sol, allNodes)


m = Model()
m.BuildModel()
solve(m)

# for ct in m.customers:
#     print(ct.id,
#         ct.service_time,
#         ct.demand,
#         ct.x,
#         ct.y,
#         ct.isRouted)

# for ct in m.allNodes:
#     print(ct.id,
#           ct.service_time,
#           ct.demand,
#           ct.x,
#           ct.y,
#           ct.isRouted)
