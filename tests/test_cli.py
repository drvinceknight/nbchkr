"""
Tests for the command line tool.
"""
import subprocess
import pathlib
import nbchkr
import csv

from test_release import NB_PATH


def test_help_call():
    output = subprocess.run(["nbchkr", "--help"], capture_output=True)
    expected_stdout = b"""Usage: nbchkr [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  check    This checks a given submission against a source.
  release  This releases a piece of coursework by removing the solutions...
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


def test_check_on_a_single_notebook():
    # TODO add better tear down.

    submission_nbs = [
        "submission.ipynb",
        "submission_with_missing_tags.ipynb",
        "test.ipynb",
    ]
    expected_outputs = [["2", "10", "True"], ["2", "10", "False"], ["10", "10", "True"]]
    for submission_nb, expected_output in zip(submission_nbs, expected_outputs):
        output = subprocess.run(
            [
                "nbchkr",
                "check",
                "--source",
                f"{NB_PATH}/test.ipynb",
                "--submitted",
                f"{NB_PATH}/{submission_nb}",
                "--feedback_suffix",
                "_feedback.md",
                "--output",
                "output.csv",
            ],
            capture_output=True,
        )
        expected_stdout = str.encode(
            f"{NB_PATH}/{submission_nb} checked against {NB_PATH}/test.ipynb. Feedback written to {NB_PATH}/{submission_nb}_feedback.md and output written to output.csv.\n"
        )
        if submission_nb == "submission_with_missing_tags.ipynb":
            expected_stdout += str.encode(
                f"WARNING: {NB_PATH}/{submission_nb} has tags that do not match the source.\n"
            )
        assert output.stdout == expected_stdout

        with open("output.csv", "r") as f:
            csv_reader = csv.reader(f)
            output = list(csv_reader)

        expected_output = [
            ["Submission filepath", "Score", "Maximum score", "Tags match"],
            [f"{NB_PATH}/{submission_nb}"] + expected_output,
        ]
        assert output == expected_output


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

    with open("output.csv", "r") as f:
        csv_reader = csv.reader(f)
        output = list(csv_reader)

    expected_output = [
        ["Submission filepath", "Score", "Maximum score", "Tags match"],
        [f"{NB_PATH}/submission.ipynb", "2", "10", "True"],
        [f"{NB_PATH}/submission_with_missing_tags.ipynb", "2", "10", "False"],
        [f"{NB_PATH}/test.ipynb", "10", "10", "True"],
    ]
    assert output == expected_output
