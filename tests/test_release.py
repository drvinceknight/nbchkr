"""
Tests for the release functionality:

    - Read in nb
    - Remove hidden/solution cells
    - Write nb

"""

import pathlib

import nbchkr.utils
import nbformat


def get_absolute_path_of_test_directory():
    return pathlib.Path(__file__).parent.absolute()


NB_PATH = get_absolute_path_of_test_directory() / "nbs/"


def test_read_nb_gives_dictionary():
    nb_path = NB_PATH / "test.ipynb"
    nb = nbchkr.utils.read(nb_path=nb_path)
    assert type(nb) is nbformat.NotebookNode


def test_read_nb_gives_expected_keys():
    nb_path = NB_PATH / "test.ipynb"
    nb = nbchkr.utils.read(nb_path=nb_path)
    expected_keys = {"cells", "metadata", "nbformat", "nbformat_minor"}
    assert set(nb.keys()) == expected_keys


def test_read_nb_cells_gives_list():
    """
    The `expected_length` variable corresponds to the number of cells in
    `tests/nbs/test.ipynb`. As new cells are added this should be updated.
    """
    nb_path = NB_PATH / "test.ipynb"
    nb = nbchkr.utils.read(nb_path=nb_path)
    expected_length = 8
    assert type(nb["cells"]) is list
    assert len(nb["cells"]) == expected_length


def test_remove_cells():
    nb_path = NB_PATH / "test.ipynb"
    nb_node = nbchkr.utils.read(nb_path=nb_path)
    student_nb = nbchkr.utils.remove_cells(nb_node=nb_node)
    expected_length = 4
    assert type(student_nb["cells"]) is list
    assert len(student_nb["cells"]) == expected_length


def test_remove_solution_and_keep_original_nb_node_unchanged():
    """
    This checks that solutions text is not included.

    Note that, as implemented both `nb_node` and `student_nb` are modified. This
    should be fixed. TODO When fixed remove this line of documentation.
    """
    nb_path = NB_PATH / "test.ipynb"
    nb_node = nbchkr.utils.read(nb_path=nb_path)
    assert "sum(i for i in range(11))" in str(nb_node)
    assert "sum(i for i in range(n + 1))" in str(nb_node)
    assert "55" in str(nb_node)
    assert "### BEGIN SOLUTION" in str(nb_node)
    assert "### END SOLUTION" in str(nb_node)

    student_nb = nbchkr.utils.remove_cells(nb_node=nb_node)
    assert "sum(i for i in range(11))" not in str(student_nb)
    assert "sum(i for i in range(n + 1))" not in str(student_nb)
    assert "55" not in str(student_nb)
    assert "BEGIN SOLUTION" in str(student_nb)
    assert "END SOLUTION" in str(student_nb)
    # TODO Add test that shows wrong behaviour of changing the imported JSON
    # and document.
    assert "sum(i for i in range(n + 1))" not in str(nb_node)


def test_write_nb():
    nb_path = NB_PATH / "test.ipynb"
    output_path = NB_PATH / "output.ipynb"
    try:
        output_path.unlink()
    except FileNotFoundError:  # TODO Ensure py3.8 is used so that can pass
        # `missing_ok=True` to `path.unlink`.
        pass
    nb_node = nbchkr.utils.read(nb_path=nb_path)
    student_nb = nbchkr.utils.remove_cells(nb_node=nb_node)
    nbchkr.utils.write(output_path=output_path, nb_node=student_nb)

    student_nb = nbchkr.utils.read(nb_path=output_path)
    assert "sum(i for i in range(11))" not in str(student_nb)
    assert "sum(i for i in range(n + 1))" not in str(student_nb)
    assert "55" not in str(student_nb)

    # TODO Add a better pytest cleanup.
    try:
        output_path.unlink()
    except FileNotFoundError:  # TODO Ensure py3.8 is used so that can pass
        # `missing_ok=True` to `path.unlink`.
        pass


def test_remove_solution_and_output_for_nb_with_hidden_problems():
    """
    This checks that solutions text is not included for
    `notebook-with-hidden-problems.ipynb` which has two bugs:

    - The output is included
    - The characters for `### BEGIN SOLUTION` are not recognized.
    """
    nb_path = NB_PATH / "specific/main-notebook-with-hidden-problems.ipynb"
    nb_node = nbchkr.utils.read(nb_path=nb_path)
    assert "permutations = tuple(itertools.permutations(animals, 3))" in str(nb_node)
    assert "0.0" in str(nb_node)

    student_nb = nbchkr.utils.remove_cells(nb_node=nb_node)
    assert "permutations = tuple(itertools.permutations(animals, 3))" not in str(
        student_nb
    )
    assert "0.0" not in str(student_nb)
