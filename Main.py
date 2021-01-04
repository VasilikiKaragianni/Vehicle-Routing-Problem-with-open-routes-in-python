from VRP_Model_Project import *

mod1 = Model()
mod1.test()
mod1.BuildModel()

mod1.test()
mod1.bestfit()
sol2 = Solution()
sol2.PrintAllRoutes()
# r = Route(0)
# s = Solution()
# r.BuildRoutes(s.all_routes)

# for i in range(0, len(mod.all_nodes)):
#     print(mod.all_nodes[i])

# for i in range(0, len(mod.all_nodes)):
#     for j in range(0, len(mod.all_nodes)):
#         print(mod.distance[i][j])
#
# for cust in mod.customers:
#     print(cust.id)

# for route in s.all_routes:
#     print(route.capacity)
