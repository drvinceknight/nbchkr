"""
Tests for the check functionality

    - Replace relevant cells with read in solutions.
    - Check scoring cells run.
    - Write feedback.

"""
import nbchkr.utils

import pathlib
import nbformat

from test_release import NB_PATH


def test_read_nb_gives_dictionary():
    nb_path = NB_PATH / "submission.ipynb"
    nb = nbchkr.utils.read(nb_path=nb_path)
    assert type(nb) is nbformat.NotebookNode


def test_add_checks_creates_notebook_with_assertions():
    nb_json = nbchkr.utils.read(nb_path=NB_PATH / "submission.ipynb")
    source_nb_json = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    nb_with_checks = nbchkr.utils.add_checks(
        nb_json=nb_json, source_nb_json=source_nb_json
    )
    assert "assert _ == 55" in str(nb_with_checks)
    assert "sum(i for i in range(10))" in str(nb_with_checks)

    output_path = NB_PATH / "feedback.ipynb"
    nbchkr.utils.write(output_path=output_path, nb_json=nb_with_checks)


def test_check_with_no_errors_for_original_source():
    nb_node = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    score,  maximum_score, feedback = nbchkr.utils.check(nb_node=nb_node)
    expected_score = 10
    assert score == expected_score
    assert maximum_score == expected_score

    expected_feedback = """
Assertion passed:

    assert _ == 55, "That is not the correct answer"

3 / 3

Assertion passed:

    assert sum_of_digits.__doc__ is not None, "You did not include a docstring"

2 / 2

Assertion passed:

    for n in range(1, 10):
    assert sum_of_digits(n=n) == n * (n + 1) / 2, f"You function did not give the correct score for n={n}"

5 / 5
"""
    assert feedback == expected_feedback


def test_check_with_no_errors_for_test_submission():
    nb_node = nbchkr.utils.read(nb_path=NB_PATH / "submission.ipynb")
    source_nb_node = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    nb_node = nbchkr.utils.add_checks(
        nb_json=nb_node, source_nb_json=source_nb_node
    )
    score,  maximum_score, feedback = nbchkr.utils.check(nb_node=nb_node)
    expected_score = 2
    expected_maximum_score = 10
    assert score == expected_score
    assert maximum_score == expected_maximum_score
    expected_feedback = """
That is not the correct answer

0 / 3

Assertion passed:

    assert sum_of_digits.__doc__ is not None, "You did not include a docstring"

2 / 2

You function did not give the correct score for n=1

0 / 5
"""
    assert feedback == expected_feedback
