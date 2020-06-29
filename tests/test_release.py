"""
Tests for the release functionality:

    - Read in nb
    - Remove hidden/solution cells
    - Write nb

"""
import nbchkr.utils

import pathlib

NB_PATH = pathlib.Path("./nbs")

def test_read_nb():
    nb_path = NB_PATH / "test.ipynb"
    nb = nbchkr.utils.read(nb_path=nb_path)
    assert type(nb) is str
