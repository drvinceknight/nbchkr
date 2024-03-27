"""
Tests for the check functionality

    - Replace relevant cells with read in solutions.
    - Check scoring cells run.
    - Write feedback.

"""

import nbchkr.utils
import nbformat
from test_release import NB_PATH


def test_read_nb_gives_dictionary():
    nb_path = NB_PATH / "submission.ipynb"
    nb = nbchkr.utils.read(nb_path=nb_path)
    assert type(nb) is nbformat.NotebookNode


def test_read_nb_gives_none_when_not_reading_notebook():
    """
    Tries to read in this test file.
    """
    nb_path = __file__
    nb = nbchkr.utils.read(nb_path=nb_path)
    assert nb == {}


def test_add_checks_creates_notebook_with_assertions():
    nb_node = nbchkr.utils.read(nb_path=NB_PATH / "submission.ipynb")
    source_nb_node = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    nb_with_checks = nbchkr.utils.add_checks(
        nb_node=nb_node, source_nb_node=source_nb_node
    )
    assert "assert _ == 55" in str(nb_with_checks)
    assert "sum(i for i in range(10))" in str(nb_with_checks)


def test_add_checks_creates_notebook_with_assertions_but_omits_missing_tags():
    nb_node = nbchkr.utils.read(nb_path=NB_PATH / "submission.ipynb")
    source_nb_node = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    nb_with_checks = nbchkr.utils.add_checks(
        nb_node=nb_node, source_nb_node=source_nb_node
    )
    assert "assert _ == 55" in str(nb_with_checks)
    assert "sum(i for i in range(10))" in str(nb_with_checks)


def test_check_with_no_errors_for_original_source():
    nb_node = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    score, maximum_score, feedback, passed_check = nbchkr.utils.check(nb_node=nb_node)
    expected_score = 10
    assert score == expected_score
    assert maximum_score == expected_score
    assert passed_check

    expected_feedback = """
---

## answer:q1

### Correct answer

3 / 3

---

## answer:q2

### Has docstring

2 / 2

### Correct answer for n up until 10

5 / 5
"""
    assert feedback == expected_feedback


def test_check_with_no_errors_for_test_submission():
    nb_node = nbchkr.utils.read(nb_path=NB_PATH / "submission.ipynb")
    source_nb_node = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    nb_node = nbchkr.utils.add_checks(nb_node=nb_node, source_nb_node=source_nb_node)
    score, maximum_score, feedback, passed_check = nbchkr.utils.check(nb_node=nb_node)
    expected_score = 2
    expected_maximum_score = 10
    assert score == expected_score
    assert maximum_score == expected_maximum_score
    expected_feedback = """
---

## answer:q1

### Correct answer

That is not the correct answer

0 / 3

---

## answer:q2

### Has docstring

2 / 2

### Correct answer for n up until 10

You function did not give the correct score for n=1

0 / 5
"""
    assert feedback == expected_feedback


def test_check_with_no_errors_for_test_submission_with_missing_tags():
    nb_node = nbchkr.utils.read(nb_path=NB_PATH / "submission_with_missing_tags.ipynb")
    source_nb_node = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    nb_node = nbchkr.utils.add_checks(nb_node=nb_node, source_nb_node=source_nb_node)
    score, maximum_score, feedback, passed_check = nbchkr.utils.check(nb_node=nb_node)
    expected_score = 2
    expected_maximum_score = 10
    expected_passed_check = {
        "Correct answer": False,
        "Correct answer for n up until 10": False,
        "Has docstring": True,
    }
    assert score == expected_score
    assert maximum_score == expected_maximum_score
    assert passed_check == expected_passed_check
    expected_feedback = """
---

## answer:q1

### Correct answer

That is not the correct answer

0 / 3

---

## answer:q2

### Has docstring

2 / 2

### Correct answer for n up until 10

You function did not give the correct score for n=1

0 / 5
"""
    assert feedback == expected_feedback
