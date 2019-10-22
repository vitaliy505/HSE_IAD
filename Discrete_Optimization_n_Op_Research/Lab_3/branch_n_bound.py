import cplex
import numpy as np
from copy import deepcopy

from constants import *


def fill_problem(_problem):
    _problem.objective.set_sense(_problem.objective.sense.maximize)

    _problem.variables.add(obj=objective,
                           lb=lower_bounds,
                           ub=upper_bounds,
                           names=names)


def solve_problem(_lin_expr, _senses, _rhs, _names):
    _problem = cplex.Cplex()
    fill_problem(_problem)
    _problem.linear_constraints.add(lin_expr=_lin_expr,
                                    senses=_senses,
                                    rhs=_rhs,
                                    names=_names)
    _problem.solve()
    return _problem.solution.get_objective_value(), _problem.solution.get_values()


def branch_n_bound(var_names, variables, coefficients, lin_constr_args, cur_objective_val, cur_variables):
    # define variables that is global for _branch_n_bound
    branch_n_bound.bnb_lower_bound = cur_objective_val
    branch_n_bound.bnb_variables = cur_variables

    def _branch_n_bound(_var_names, _variables, _coefficients, _lin_constr_args, _cur_objective_val, _cur_variables):
        # Finish branching if current objective value less than bnb_lower_bound
        # (because future objective values also will be less)
        if _cur_objective_val < branch_n_bound.bnb_lower_bound:
            return

        # Step 1: find variables with real value
        real_vars_inds = [i for i, _var in enumerate(_variables) if int(_var) != _var]
        # Step 2: if solution has only integer variables, compute new bnb_lower_bound
        # and stop computation in current branch
        if len(real_vars_inds) == 0:
            if _cur_objective_val > branch_n_bound.bnb_lower_bound:
                branch_n_bound.bnb_lower_bound = _cur_objective_val
                branch_n_bound.bnb_variables = _cur_variables
            return
        # Step 3: find variable with max coefficient to start maximization
        var_w_max_coeff_ind = np.argmax([c for c in [_coefficients[i] for i in real_vars_inds]])

        # Step 4: find values for future constrains
        constraint_var1 = int(_variables[var_w_max_coeff_ind])
        constraint_var2 = int(_variables[var_w_max_coeff_ind]) + 1

        # Step 5: solve the first problem with additional constraint and start branching
        lin_constr_args1 = deepcopy(_lin_constr_args)
        lin_constr_arg = [[[_var_names[var_w_max_coeff_ind]], [1.0]], "L", constraint_var1, "not_unique_name"]
        for ind, arg in enumerate(lin_constr_args1):
            arg.append(lin_constr_arg[ind])
        for ind, arg in enumerate(lin_constr_args1):
            arg.append(lin_constr_arg[ind])
        try:
            objective_val1, variables1 = solve_problem(lin_constr_args1[0], lin_constr_args1[1], lin_constr_args1[2],
                                                       lin_constr_args1[3])
            _branch_n_bound(var_names, variables1, _coefficients, lin_constr_args1, objective_val1, variables1)
        except Exception as e:
            if "No solution exists." in repr(e):
                print(repr(e))
            else:
                raise

        # Step 6: solve the second problem with additional constraint and start branching
        lin_constr_args2 = deepcopy(_lin_constr_args)
        lin_constr_arg = [[[var_names[var_w_max_coeff_ind]], [1.0]], "G", constraint_var2, "not_unique_name"]
        for ind, arg in enumerate(lin_constr_args2):
            arg.append(lin_constr_arg[ind])
        try:
            objective_val2, variables2 = solve_problem(lin_constr_args2[0], lin_constr_args2[1], lin_constr_args2[2],
                                                       lin_constr_args2[3])
            _branch_n_bound(var_names, variables2, _coefficients, lin_constr_args2, objective_val2, variables2)
        except Exception as e:
            if "No solution exists." in repr(e):
                print(repr(e))
            else:
                raise

    _branch_n_bound(var_names, variables, coefficients, lin_constr_args, cur_objective_val, cur_variables)
    return branch_n_bound.bnb_lower_bound, branch_n_bound.bnb_variables
