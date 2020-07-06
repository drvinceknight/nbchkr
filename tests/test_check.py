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
