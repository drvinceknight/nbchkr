"""
Tests for the release functionality:

    - Read in nb
    - Remove hidden/solution cells
    - Write nb

"""
import nbchkr.utils

import pathlib

def get_absolute_path_of_test_directory():
    return pathlib.Path(__file__).parent.absolute()


NB_PATH = get_absolute_path_of_test_directory() / "nbs/"


def test_read_nb_gives_dictionary():
    nb_path = NB_PATH / "test.ipynb"
    nb = nbchkr.utils.read(nb_path=nb_path)
    assert type(nb) is dict


def test_read_nb_gives_expected_keys():
    nb_path = NB_PATH / "test.ipynb"
    nb = nbchkr.utils.read(nb_path=nb_path)
    expected_keys = {
            'cells',
            'metadata',
            'nbformat',
            'nbformat_minor',
            }
    assert set(nb.keys()) == expected_keys


def test_read_nb_cells_gives_list():
    """
    The `expected_length` variable corresponds to the number of cells in
    `tests/nbs/test.ipynb`. As new cells are added this should be updated.
    """
    nb_path = NB_PATH / "test.ipynb"
    nb = nbchkr.utils.read(nb_path=nb_path)
    expected_length = 2
    assert type(nb["cells"]) is list
    assert len(nb["cells"]) == expected_length
