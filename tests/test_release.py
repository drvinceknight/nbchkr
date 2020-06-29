"""
Tests for the release functionality:

    - Read in nb
    - Remove hidden/solution cells
    - Write nb

"""
import nbchkr

import pathlib

NB_PATH = pathlib.Path("./nbs")

def test_read_nb():
    path = NB_PATH / "test.ipynb"
    nb = nbchkr.utils.read(path=path)
    assert type(nb) is str
