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
