"""
A lightweight solution to mark/grade/check notebook assignments.
"""

from .checks import (
    NbChkrIncorrectVariable,
    NbChkrVariableDoesNotExist,
    check_variable_has_expected_property,
)

__version__ = "0.0.8"
