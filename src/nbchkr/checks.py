"""
This module contains code that can be used to write checks.

All code that does not pass a given check raises one of two types of errors:
"""

import sys


class NbChkrVariableDoesNotExist(Exception):
    pass


class NbChkrIncorrectVariable(Exception):
    pass


def check_variable_has_expected_property(
    variable_string, feedback_string, property_check, **property_check_kwargs
):
    local_variables = sys._getframe(1).f_locals
    if variable_string not in local_variables:
        raise NbChkrVariableDoesNotExist(
            f"The variable {variable_string} does not exist."
        )
    try:
        variable = local_variables[variable_string]
        assert property_check(variable=variable, **property_check_kwargs)
    except AssertionError:
        raise NbChkrIncorrectVariable(
            f"Your variable {variable_string} has value {variable}.\n {feedback_string}"
        )
