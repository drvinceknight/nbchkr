"""
Tests for the command line tool.
"""
import subprocess
import pathlib
import nbchkr

from test_release import NB_PATH

def test_help_call():
    output = subprocess.run(["nbchkr", "--help"], capture_output=True)
    expected_stdout = b"""Usage: nbchkr [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  release
"""
    assert output.stdout == expected_stdout
    assert output.stderr == b''

def test_release():
    # TODO Add better tear down.
    output = subprocess.run(["nbchkr", "release", "--source", f"{NB_PATH}/test.ipynb", "--output", "student.ipynb"], capture_output=True)
    expected_stdout = str.encode(f'Solutions removed from {NB_PATH}/test.ipynb. New notebook written to student.ipynb.\n')
    assert output.stderr == b''
    assert output.stdout == expected_stdout

    student_nb = nbchkr.utils.read(nb_path="student.ipynb")
    expected_length = 4
    assert type(student_nb["cells"]) is list
    assert len(student_nb["cells"]) == expected_length
    # TODO Add a better pytest cleanup.
    try:
        pathlib.Path("student.ipynb").unlink()
    except FileNotFoundError:  # TODO Ensure py3.8 is used so that can pass
        # `missing_ok=True` to `path.unlink`.
        pass
