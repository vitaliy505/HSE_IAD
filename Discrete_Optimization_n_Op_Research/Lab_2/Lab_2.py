import cplex
import numpy as np

# Create an instance of a linear problem to solve
problem = cplex.Cplex()

# We want to find a maximum of our objective function
problem.objective.set_sense(problem.objective.sense.maximize)

# The names of our variables
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
D = np.array([1000.0, 2000.0, 900.0, 1200.0])

C = np.array([[1000.0, 1100.0, 1200.0, 1500.0],
              [800.0, 900.0, 1000.0, 1000.0],
              [600.0, 800.0, 800.0, 900.0]])
P = np.array([40.0, 50.0, 45.0, 70.0])

# The objective function. More precisely, the coefficients of the objective
# function. Note that we are casting to floats.

# objective = [6000, 5000, 4500, 3500,
#              4800, 4500, 4050, 4200,
#              4000, 5000, 3600, 2800,
#              -3000, -2200, -2400, -1500,
#              -3200, -2700, -3000, -2000,
#              -3000, -4000, -3200, -1800]
Z = np.array([Q * T[:, i] * P[i] for i in range(4)]).T
objective = list(np.array([Z, -T * C]).flatten())

# Lower bounds. Since these are all zero, we could simply not pass them in as
# all zeroes is the default.
lower_bounds = [0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0]

# Upper bounds. The default here would be cplex.infinity, or 1e+20.
upper_bounds = [cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity,
                cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity,
                cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity,
                cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity,
                cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity,
                cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity]

problem.variables.add(obj=objective,
                      lb=lower_bounds,
                      ub=upper_bounds,
                      names=names)

# Constraints

# Constraints are entered in two parts, as a left hand part and a right hand
# part. Most times, these will be represented as matrices in your problem. In
# our case, we have "3x + y - z ≤ 75" and "3x + 4y + 4z ≤ 160" which we can
# write as matrices as follows:

# [  3   1  -1 ]   [ x ]   [  75 ]
# [  3   4   4 ]   [ y ] ≤ [ 160 ]
#                  [ z ]

# First, we name the constraints
constraint_names = ["n1", "n2", "n3",
                    "d1", "d2", "d3", "d4",
                    "xy11", "xy12", "xy13", "xy14",
                    "xy21", "xy22", "xy23", "xy24",
                    "xy31", "xy32", "xy33", "xy34"]

# The actual constraints are now added. Each constraint is actually a list
# consisting of two objects, each of which are themselves lists. The first list
# represents each of the variables in the constraint, and the second list is the
# coefficient of the respective variable. Data is entered in this way as the
# constraints matrix is often sparse.

# Constraint is entered by referring to each variable by its name
# (which we defined earlier). This then represents "3x + y - z"

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

# So far we haven't added a right hand side, so we do that now. Note that the
# first entry in this list corresponds to the first constraint, and so-on.
rhs = [N[0], N[1], N[2],  # for constraint_n#
       D[0], D[1], D[2], D[3],  # for constraint_d#
       0.0, 0.0, 0.0, 0.0,  # for constraint_xy##
       0.0, 0.0, 0.0, 0.0,  # for constraint_xy##
       0.0, 0.0, 0.0, 0.0  # for constraint_xy##
       ]

# We need to enter the senses of the constraints. That is, we need to tell Cplex
# whether each constrains should be treated as an upper-limit (≤, denoted "L"
# for less-than), a lower limit (≥, denoted "G" for greater than) or an equality
# (=, denoted "E" for equality)
constraint_senses = ["L", "L", "L",
                     "L", "L", "L", "L",
                     "L", "L", "L", "L",
                     "L", "L", "L", "L",
                     "L", "L", "L", "L"]

# And add the constraints
problem.linear_constraints.add(lin_expr=constraints,
                               senses=constraint_senses,
                               rhs=rhs,
                               names=constraint_names)

# Solve the problem
problem.solve()
variables = problem.solution.get_values()

# And print the solutions
print("F*: {}\n".format(problem.solution.get_objective_value()))

print("Variables:")
print("x11: {}, x12: {}, x13: {}, x14: {}".format(variables[0], variables[1], variables[2], variables[3]))
print("x21: {}, x22: {}, x23: {}, x24: {}".format(variables[4], variables[5], variables[6], variables[7]))
print("x31: {}, x32: {}, x33: {}, x34: {}".format(variables[8], variables[9], variables[10], variables[11]))
print("y11: {}, y12: {}, y13: {}, y14: {}".format(variables[12], variables[13], variables[14], variables[15]))
print("y21: {}, y22: {}, y23: {}, y24: {}".format(variables[16], variables[17], variables[18], variables[19]))
print("y31: {}, y32: {}, y33: {}, y34: {}".format(variables[20], variables[21], variables[22], variables[23]))

dual_variables = problem.solution.get_dual_values()
print("\nDual Variables:")
print("m1: {}, m2: {}, m3: {}".format(dual_variables[0], dual_variables[1], dual_variables[2]))
print(
    "k1: {}, k2: {}, k3: {}, k4: {}".format(dual_variables[3], dual_variables[4], dual_variables[5], dual_variables[6]))
print("z1: {}, z2: {}, z3: {}, z4: {}".format(dual_variables[7], dual_variables[8], dual_variables[9],
                                              dual_variables[10]))
print("z5: {}, z6: {}, z7: {}, z8: {}".format(dual_variables[11], dual_variables[12], dual_variables[13],
                                              dual_variables[14]))
print("z9: {}, z10: {}, z11 {}, z12: {}".format(dual_variables[15], dual_variables[16], dual_variables[17],
                                                dual_variables[18]))

# Tables below was used to model constraints for dual problem
straight_problem = np.array([
#    y11, y12, y13, y14, y21, y22, y23, y24, y31, y32, y33, y34, x11, x12, x13, x14, x21, x22, x23, x24, x31, x32, x33, x34
     [1,   1,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   1,   1,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1],

     [-1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
     [0,   -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
     [0,   0,   -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   0,   -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1]])

dual_problem = [
#  m1,  m2,  m3,  k1,  k2,  k3,  k4,  z1,  z2,  z3,  z4,  z5,  z6  ,z7,  z8,  z9,  z10, z11, z12
 [ 1,   0,   0,   0,   0,   0,   0,  -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
 [ 1,   0,   0,   0,   0,   0,   0,   0,  -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
 [ 1,   0,   0,   0,   0,   0,   0,   0,   0,  -1,   0,   0,   0,   0,   0,   0,   0,   0,   0],
 [ 1,   0,   0,   0,   0,   0,   0,   0,   0,   0,  -1,   0,   0,   0,   0,   0,   0,   0,   0],
 [ 0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,  -1,   0,   0,   0,   0,   0,   0,   0],
 [ 0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  -1,   0,   0,   0,   0,   0,   0],
 [ 0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  -1,   0,   0,   0,   0,   0],
 [ 0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  -1,   0,   0,   0,   0],
 [ 0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  -1,   0,   0,   0],
 [ 0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  -1,   0,   0],
 [ 0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  -1,   0],
 [ 0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  -1],
 [ 0,   0,   0,   1,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
 [ 0,   0,   0,   1,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
 [ 0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0],
 [ 0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0],
 [ 0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0],
 [ 0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0],
 [ 0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0],
 [ 0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0],
 [ 0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0],
 [ 0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0],
 [ 0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0],
 [ 0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1]]
