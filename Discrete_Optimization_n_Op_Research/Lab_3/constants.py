import cplex
import numpy as np

names = ["x11", "x12", "x13", "x14",
         "x21", "x22", "x23", "x24",
         "x31", "x32", "x33", "x34",
         "y11", "y12", "y13", "y14",
         "y21", "y22", "y23", "y24",
         "y31", "y32", "y33", "y34"]

T = np.array([[3.0, 2.0, 2.0, 1.0],
              [4.0, 3.0, 3.0, 2.0],
              [5.0, 5.0, 4.0, 2.0]])
Q = np.array([50.0, 30.0, 20.0])
N = np.array([5.0, 8.0, 10.0])
D = np.array([700.0, 1500.0, 700.0, 1500.0])

C = np.array([[1000.0, 1100.0, 1200.0, 1500.0],
              [800.0, 900.0, 1000.0, 1000.0],
              [600.0, 800.0, 800.0, 900.0]])
P = np.array([40.0, 50.0, 45.0, 70.0])

# Example with deep branching:
# T = np.array([[3.0, 2.0, 2.0, 7.0],
#               [4.0, 3.0, 1.0, 2.0],
#               [7.0, 2.0, 4.0, 2.0]])
# Q = np.array([52.0, 29.0, 13.0])
# N = np.array([5.0, 8.0, 10.0])
# D = np.array([530.0, 1720.0, 780.0, 1530.0])
#
# C = np.array([[1000.0, 1100.0, 1200.0, 1500.0],
#               [800.0, 900.0, 1000.0, 1000.0],
#               [600.0, 800.0, 800.0, 900.0]])
# P = np.array([42.0, 39.0, 45.0, 69.0])

Z = np.array([Q * T[:, i] * P[i] for i in range(4)]).T
objective = list(np.array([Z, -T * C]).flatten())

lower_bounds = [0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0]

upper_bounds = [cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity,
                cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity,
                cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity,
                cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity,
                cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity,
                cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity]






constraint_names = ["n1", "n2", "n3",
                    "d1", "d2", "d3", "d4",
                    "xy11", "xy12", "xy13", "xy14",
                    "xy21", "xy22", "xy23", "xy24",
                    "xy31", "xy32", "xy33", "xy34"]

constraint_n1 = [["y11", "y12", "y13", "y14"], [1.0, 1.0, 1.0, 1.0]]
constraint_n2 = [["y21", "y22", "y23", "y24"], [1.0, 1.0, 1.0, 1.0]]
constraint_n3 = [["y31", "y32", "y33", "y34"], [1.0, 1.0, 1.0, 1.0]]

constraint_d1 = [["x11", "x21", "x31"], [Q[0] * T[0][0], Q[1] * T[1][0], Q[2] * T[2][0]]]
constraint_d2 = [["x12", "x22", "x32"], [Q[0] * T[0][1], Q[1] * T[1][1], Q[2] * T[2][1]]]
constraint_d3 = [["x13", "x23", "x33"], [Q[0] * T[0][2], Q[1] * T[1][2], Q[2] * T[2][2]]]
constraint_d4 = [["x14", "x24", "x34"], [Q[0] * T[0][3], Q[1] * T[1][3], Q[2] * T[2][3]]]

constraint_xy11 = [["x11", "y11"], [1.0, -1.0]]
constraint_xy12 = [["x12", "y12"], [1.0, -1.0]]
constraint_xy13 = [["x13", "y13"], [1.0, -1.0]]
constraint_xy14 = [["x14", "y14"], [1.0, -1.0]]
constraint_xy21 = [["x21", "y21"], [1.0, -1.0]]
constraint_xy22 = [["x22", "y22"], [1.0, -1.0]]
constraint_xy23 = [["x23", "y23"], [1.0, -1.0]]
constraint_xy24 = [["x24", "y24"], [1.0, -1.0]]
constraint_xy31 = [["x31", "y31"], [1.0, -1.0]]
constraint_xy32 = [["x32", "y32"], [1.0, -1.0]]
constraint_xy33 = [["x33", "y33"], [1.0, -1.0]]
constraint_xy34 = [["x34", "y34"], [1.0, -1.0]]

constraints = [constraint_n1, constraint_n2, constraint_n3,
               constraint_d1, constraint_d2, constraint_d3, constraint_d4,
               constraint_xy11, constraint_xy12, constraint_xy13, constraint_xy14,
               constraint_xy21, constraint_xy22, constraint_xy23, constraint_xy24,
               constraint_xy31, constraint_xy32, constraint_xy33, constraint_xy34]

rhs = [N[0], N[1], N[2],  # for constraint_n#
       D[0], D[1], D[2], D[3],  # for constraint_d#
       0.0, 0.0, 0.0, 0.0,  # for constraint_xy##
       0.0, 0.0, 0.0, 0.0,  # for constraint_xy##
       0.0, 0.0, 0.0, 0.0  # for constraint_xy##
       ]

constraint_senses = ["L", "L", "L",
                     "L", "L", "L", "L",
                     "L", "L", "L", "L",
                     "L", "L", "L", "L",
                     "L", "L", "L", "L"]