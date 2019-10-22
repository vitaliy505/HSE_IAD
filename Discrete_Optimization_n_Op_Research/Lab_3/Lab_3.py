import cplex
import sys
import logging as log
log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)

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

real_vars = [var for var in variables if int(var) != var]
if len(real_vars) == 0:
    log.info("Solution contains only integer variables. Problem was solved.")
    objective_value = problem.solution.get_objective_value()
else:
    log.info("Solution contains float variables. Start 'branch and bound' method to find solution "
             "with only integer values.")
    objective_value, variables = branch_n_bound(names, variables, objective,
                                                [constraints, constraint_senses, rhs, constraint_names],
                                                bnb_lower_bound,
                                                bnb_variables)
    if not variables:
        log.info("Solution wasn't found.")
        exit()

log.info("F*: {}\n".format(objective_value))

log.info("Variables:")
log.info("x11: {}, x12: {}, x13: {}, x14: {}".format(variables[0], variables[1], variables[2], variables[3]))
log.info("x21: {}, x22: {}, x23: {}, x24: {}".format(variables[4], variables[5], variables[6], variables[7]))
log.info("x31: {}, x32: {}, x33: {}, x34: {}".format(variables[8], variables[9], variables[10], variables[11]))
log.info("y11: {}, y12: {}, y13: {}, y14: {}".format(variables[12], variables[13], variables[14], variables[15]))
log.info("y21: {}, y22: {}, y23: {}, y24: {}".format(variables[16], variables[17], variables[18], variables[19]))
log.info("y31: {}, y32: {}, y33: {}, y34: {}".format(variables[20], variables[21], variables[22], variables[23]))
