import nbchkr.checks
import pytest


def test_check_function_raises_NbChkrVariableDoesNotExist():
    variable_string = "number"
    feedback_string = "Your number is not an integer"

    def property_check(variable):
        return type(variable) is int

    with pytest.raises(
        nbchkr.checks.NbChkrVariableDoesNotExist,
        match="The variable number does not exist.",
    ):
        nbchkr.checks.check_variable_has_expected_property(
            variable_string=variable_string,
            feedback_string=feedback_string,
            property_check=property_check,
        )


def test_check_function_raises_NbChkrIncorrectVariable():
    variable_string = "number"
    feedback_string = "Your number is not an integer"
    number = 2.6

    def property_check(variable):
        return type(variable) is int

    with pytest.raises(
        nbchkr.checks.NbChkrIncorrectVariable,
        match=f"Your variable number has value 2.6.\n Your number is not an integer",
    ):
        nbchkr.checks.check_variable_has_expected_property(
            variable_string=variable_string,
            feedback_string=feedback_string,
            property_check=property_check,
        )
