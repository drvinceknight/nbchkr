"""
Tests for the command line tool.
"""
import subprocess
import pathlib
import nbchkr
import filecmp

from test_release import NB_PATH


def test_help_call():
    output = subprocess.run(["nbchkr", "--help"], capture_output=True)
    expected_stdout = b"""Usage: nbchkr [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  check
  release
"""
    assert output.stdout == expected_stdout
    assert output.stderr == b""


def test_release():
    # TODO Add better tear down.
    output = subprocess.run(
        [
            "nbchkr",
            "release",
            "--source",
            f"{NB_PATH}/test.ipynb",
            "--output",
            "student.ipynb",
        ],
        capture_output=True,
    )
    expected_stdout = str.encode(
        f"Solutions removed from {NB_PATH}/test.ipynb. New notebook written to student.ipynb.\n"
    )
    assert output.stderr == b""
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


# def test_check_on_a_single_notebook():
# # TODO Add better tear down.
# output = subprocess.run(["nbchkr", "check", "--source",
# f"{NB_PATH}/test.ipynb", "--submitted", f"{NB_PATH}/submission.ipynb", "--feedback_suffix", "_feedback.md", "--output", "output.csv"], capture_output=True)
# expected_stdout = str.encode(f'{NB_PATH}/submission.ipynb checked against {NB_PATH}/test.ipynb. Feedback written to {NB_PATH}/submission.ipynb_feedback.md and output written to output.csv.\n')
# # assert output.stderr == b''  # TODO Fix the warning error
# assert output.stdout == expected_stdout


def test_check_on_a_collection_of_notebooks():
    # TODO Add better tear down.
    output = subprocess.run(
        [
            "nbchkr",
            "check",
            "--source",
            f"{NB_PATH}/test.ipynb",
            "--submitted",
            f"{NB_PATH}/*.ipynb",
            "--feedback_suffix",
            "_feedback.md",
            "--output",
            "output.csv",
        ],
        capture_output=True,
    )
    expected_stdout = str.encode(
        f"{NB_PATH}/submission.ipynb checked against {NB_PATH}/test.ipynb. Feedback written to {NB_PATH}/submission.ipynb_feedback.md and output written to output.csv.\n"
    )
    expected_stdout += str.encode(
        f"{NB_PATH}/submission_with_missing_tags.ipynb checked against {NB_PATH}/test.ipynb. Feedback written to {NB_PATH}/submission_with_missing_tags.ipynb_feedback.md and output written to output.csv.\n"
    )
    expected_stdout += str.encode(
        f"WARNING: {NB_PATH}/submission_with_missing_tags.ipynb has tags that do not match the source.\n"
    )
    expected_stdout += str.encode(
        f"{NB_PATH}/test.ipynb checked against {NB_PATH}/test.ipynb. Feedback written to {NB_PATH}/test.ipynb_feedback.md and output written to output.csv.\n"
    )
    # assert output.stderr == b''  # TODO Fix the warning error
    assert output.stdout == expected_stdout
    assert filecmp.cmp(
        f1="output.csv", f2=f"{NB_PATH}/expected_output.csv", shallow=True
    )
