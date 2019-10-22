import cplex
from constants import *
from branch_n_bound import fill_problem, branch_n_bound

# Solve the problem simple way to find bnb_upper_bound
problem = cplex.Cplex()
fill_problem(problem)
problem.linear_constraints.add(lin_expr=constraints,
                               senses=constraint_senses,
                               rhs=rhs,
                               names=constraint_names)
problem.solve()

variables = problem.solution.get_values()

bnb_upper_bound = problem.solution.get_objective_value()
bnb_lower_bound = -1e+20
bnb_variables = []

objective_value, variables = branch_n_bound(names, variables, objective,
                                            [constraints, constraint_senses, rhs, constraint_names], bnb_lower_bound,
                                            bnb_variables)
if variables:
    print("F*: {}\n".format(objective_value))

    print("Variables:")
    print("x11: {}, x12: {}, x13: {}, x14: {}".format(variables[0], variables[1], variables[2], variables[3]))
    print("x21: {}, x22: {}, x23: {}, x24: {}".format(variables[4], variables[5], variables[6], variables[7]))
    print("x31: {}, x32: {}, x33: {}, x34: {}".format(variables[8], variables[9], variables[10], variables[11]))
    print("y11: {}, y12: {}, y13: {}, y14: {}".format(variables[12], variables[13], variables[14], variables[15]))
    print("y21: {}, y22: {}, y23: {}, y24: {}".format(variables[16], variables[17], variables[18], variables[19]))
    print("y31: {}, y32: {}, y33: {}, y34: {}".format(variables[20], variables[21], variables[22], variables[23]))
else:
    print("Solution wasn't found")
