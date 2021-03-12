# Vehicle Routing Problem with open routes in python

This repository contains a solution to the Vehicle Routing Problem (VRP) in python.
In this problem there are 100 customers to be served and a main depot. 
Each customer asks for products of a specific weight.
In the depot there are 15 vehicles with capacity of 1500kg and 15 vehicles with capacity of 1200kg.
The vehicles travel at 35km/h and the unloading time of goods in every stop is 15 minutes.
Our goal is to satisfy all customers by creating routes using the vehicles we have.
One customer will be visited and satisfied by only one vehicle.
Each route starts at the depot and finishes at the last customer(open routes) and should not last longer than 3.5h.

Obgective: Minimize the total distance of all routes

In order to solve this problem we wrote a modified version of the Apply Nearest Neighbour algorithm. In this method we find the closest node to the depot and add it to the route if the time and capacity constraints are met. If not we move on to the next nearest neighbour node and check again. Once the first route is created we find the closest node to the depot that we haven't visited yet and repeat as described above. The process is repeated until all routes are created. Our initial solution had an obgective: distance= 1629.

Then we decided to improve our initial solution by writing a modified version of the Local Search algorithm using the move type: Relocation.The algorithm checks all the possible relocations of the already constructed routes. The code was modified in order to satisfy open routes.
After the application of this algorithm our objective dropped at distance = 1403.

At last, we decide to give our algorithm a final touch by applying a modifiled version of the Variable neighborhood search algorithm. The VND method uses three move types: Relocation, Two-Opt and Swap-Move. In the Two-Opt, the method will compare every possible valid combination of the swapping mechanism. In the Swap-Move, the method checks all the possible swaps of the already constructed routes. The code was modified in order to satisfy open routes. We tried all the 6 possible combinations of move types, such as R-S-2.
After the application of this algorithm our objective dropped at distance = 1267 and the best combination was S-2-R.

We hope this project has proven useful! 
Thanks for reading!

