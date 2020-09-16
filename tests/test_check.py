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
    score, maximum_score, feedback = nbchkr.utils.check(nb_node=nb_node)
    expected_score = 10
    assert score == expected_score
    assert maximum_score == expected_score

    expected_feedback = """
---

## answer:q1

3 / 3

---

## answer:q2

2 / 2

5 / 5
"""
    assert feedback == expected_feedback


def test_check_with_no_errors_for_test_submission():
    nb_node = nbchkr.utils.read(nb_path=NB_PATH / "submission.ipynb")
    source_nb_node = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    nb_node = nbchkr.utils.add_checks(nb_node=nb_node, source_nb_node=source_nb_node)
    score, maximum_score, feedback = nbchkr.utils.check(nb_node=nb_node)
    expected_score = 2
    expected_maximum_score = 10
    assert score == expected_score
    assert maximum_score == expected_maximum_score
    expected_feedback = """
---

## answer:q1

That is not the correct answer

0 / 3

---

## answer:q2

2 / 2

You function did not give the correct score for n=1

0 / 5
"""
    assert feedback == expected_feedback


def test_check_with_no_errors_for_test_submission_with_missing_tags():
    nb_node = nbchkr.utils.read(nb_path=NB_PATH / "submission_with_missing_tags.ipynb")
    source_nb_node = nbchkr.utils.read(nb_path=NB_PATH / "test.ipynb")
    nb_node = nbchkr.utils.add_checks(nb_node=nb_node, source_nb_node=source_nb_node)
    score, maximum_score, feedback = nbchkr.utils.check(nb_node=nb_node)
    expected_score = 2
    expected_maximum_score = 10
    assert score == expected_score
    assert maximum_score == expected_maximum_score
    expected_feedback = """
---

## answer:q1

That is not the correct answer

0 / 3

---

## answer:q2

2 / 2

You function did not give the correct score for n=1

0 / 5
"""
    assert feedback == expected_feedback
