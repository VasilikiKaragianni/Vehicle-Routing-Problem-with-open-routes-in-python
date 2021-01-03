import random
import math
import numpy as np


class Model:

    # instance variables
    def __init__(self):
        self.all_nodes = []
        self.customers = []
        self.distance = []
        self.time = []

        self.numberOf1500 = 15
        self.numberOf1200 = 15
        # self.capacity = -1

    def test(self):
        print(len(self.customers))
        print(len(self.all_nodes))

    def BuildModel(self):
        # birthday 08/02/1999
        birthday = 8021999
        random.seed(birthday)
        self.all_nodes = []
        self.customers = []
        depot = Node(0, 0, 0, 50, 50)
        self.all_nodes.append(depot)
        random.seed(1)
        for i in range(0, 100):
            id = i + 1
            dem = random.randint(1, 5) * 100
            xx = random.randint(0, 100)
            yy = random.randint(0, 100)
            st = 0.25  # 15 minutes in hrs
            cust = Node(id, st, dem, xx, yy)
            self.all_nodes.append(cust)
            self.customers.append(cust)

        self.distance = [[0.0 for j in range(0, len(self.all_nodes))] for k in range(0, len(self.all_nodes))]
        self.time = [[0.0 for j in range(0, len(self.all_nodes))] for k in range(0, len(self.all_nodes))]

        for i in range(0, len(self.all_nodes)):
            for j in range(0, len(self.all_nodes)):
                source = self.all_nodes[i]
                target = self.all_nodes[j]
                dx_2 = (source.x - target.x) ** 2
                dy_2 = (source.y - target.y) ** 2
                dist = round(math.sqrt(dx_2 + dy_2))
                self.distance[i][j] = dist
                self.time[i][j] = dist/35 + 0.25
                self.time[i][j] = round(self.time[i][j], 2)
                # print(distance[i][j])
                # print(time[i][j])

        sol = Solution()
        # print(len(sol.all_routes))
        # print(len(customers))
        # print(len(all_nodes))
        print(len(self.customers))
        print(len(self.all_nodes))
        a = np.asarray(self.distance)
        np.savetxt("distance.csv", a, fmt="%d", delimiter=",")

        b = np.asarray(self.time)
        np.savetxt("time.csv", b, fmt="%d", delimiter=",")

    def bestfit(self):

        sol = Solution()
        firstRoute = Route(1500)
        depot = Node(0, 0, 0, 50, 50)
        firstRoute.sequenceOfNodes.append(depot)
        sol.all_routes.append(firstRoute)
        # print(firstRoute.load,
        #     firstRoute.capacity,
        #     firstRoute.time,
        #     firstRoute.timeleft,
        #     firstRoute.maxtime,
        #     firstRoute.distance)
        mod = Model()
        print(len(sol.all_routes))
        print(len(self.customers))
        print(len(self.all_nodes))
        self.customers.sort(key=lambda x: x.demand, reverse=True)

        served  = 0
        for cust in self.customers:
            found = False

            if self.numberOf1500 > 1:
                minTime = 3.6
                timeAdded = 0
                distanceAdded = 0
                routeToBeInserted = None
                minEmptySpace = 1501
                for route in sol.all_routes:
                    if cust.demand + route.load <= 1500:
                        lastcust = route.sequenceOfNodes[-1]
                        i = cust.id
                        j = lastcust.id
                        if self.time[j][i] + route.time <= 3.5:
                            found = True
                            # print(found)
                            # print(route.timeleft)
                            # print(minTime)
                            if (1500 - route.load) < minEmptySpace:
                            # if route.timeleft < minTime:
                            #     minTime = route.timeleft
                                minEmptySpace = 1500 - route.load
                                routeToBeInserted = route
                                timeAdded = self.time[j][i]
                                distanceAdded = self.distance[j][i]
                # print(found)
                if found == True:
                    routeToBeInserted.load += cust.demand
                    routeToBeInserted.time += timeAdded
                    routeToBeInserted.timeleft -= timeAdded
                    routeToBeInserted.distance += distanceAdded
                    cust.isRouted = True
                    routeToBeInserted.sequenceOfNodes.append(cust)
                else:
                    newRoute = Route(1500)
                    newRoute.sequenceOfNodes.append(depot)
                    sol.all_routes.append(newRoute)
                    self.numberOf1500 -= 1

                    lastcust = route.sequenceOfNodes[-1]
                    i = cust.id
                    j = lastcust.id
                    timeAdded = self.time[j][i]
                    distanceAdded = self.distance[j][i]
                    newRoute.load += cust.demand
                    newRoute.time += timeAdded
                    newRoute.timeleft -= timeAdded
                    newRoute.distance += distanceAdded
                    cust.isRouted = True
                    newRoute.sequenceOfNodes.append(cust)

                served +=1
            elif self.numberOf1200 > 0:
                minTime = 3.5
                timeAdded = 0
                distanceAdded = 0
                minEmptySpace = 1201
                for route in sol.all_routes:
                    if cust.demand + route.load <= 1500:
                        lastcust = route.sequenceOfNodes[-1]
                        i = cust.id
                        j = lastcust.id
                        if self.time[j][i] + route.time <= 3.5:
                            found = True
                            if (1200 - route.load) < minEmptySpace:
                            # if route.timeleft < minTime:
                            #     minTime = route.timeleft
                                minEmptySpace = 1200 - route.load
                                routeToBeInserted = route
                                timeAdded = self.time[j][i]
                                distanceAdded = self.distance[j][i]

                if found == True:
                    routeToBeInserted.load += cust.demand
                    routeToBeInserted.time += timeAdded
                    routeToBeInserted.timeleft -= timeAdded
                    routeToBeInserted.distance += distanceAdded
                    cust.isRouted = True
                    routeToBeInserted.sequenceOfNodes.append(cust)
                else:
                    newRoute = Route(1200)
                    newRoute.sequenceOfNodes.append(depot)
                    sol.all_routes.append(newRoute)
                    self.numberOf1200 -= 1

                    lastcust = route.sequenceOfNodes[-1]
                    i = cust.id
                    j = lastcust.id
                    timeAdded = self.time[j][i]
                    distanceAdded = self.distance[j][i]
                    newRoute.load += cust.demand
                    newRoute.time += timeAdded
                    newRoute.timeleft -= timeAdded
                    newRoute.distance += distanceAdded
                    cust.isRouted = True
                    newRoute.sequenceOfNodes.append(cust)

                served += 1
            else:
                break

        print(len(sol.all_routes))
        print(len(self.customers))
        print(len(self.all_nodes))

        for ct in self.customers:
            print(ct.demand)
        # for rt in sol.all_routes:
        #     print(rt.load, rt.capacity, rt.time, rt.timeleft, rt.maxtime, rt.distance)
        #
        # for rt in sol.all_routes:
        #     print(rt.load, rt.capacity, rt.time, rt.timeleft, rt.maxtime, rt.distance)
        #     for n in rt.sequenceOfNodes:
        #         print(n.id)
        #
        # for ct in self.customers:
        #     print(ct.isRouted)
        print(served)



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
        ##self.sequenceOfNodes.append(dp)
        ##self.sequenceOfNodes.append(dp)
        self.load = 0
        self.capacity = cap
        self.time = 0
        self.timeleft = 3.5
        self.maxtime = 3.5
        self.distance = 0

    # def BuildRoutes(self, all_routes):
    #     for i in range(0, 30):
    #         r = Route(1500)
    #         all_routes.append(r)
    #     for i in range(0, 30):
    #         r = Route(1200)
    #         all_routes.append(r)

class Solution:
    def __init__(self):
        self.all_routes = []
        self.allTime = 0
        self.allDist = 0


