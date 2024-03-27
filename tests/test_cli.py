"""
Tests for the command line tool.
"""

import csv
import pathlib
import subprocess

import nbchkr
from test_release import NB_PATH


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
        f"Solutions and checks removed from {NB_PATH}/test.ipynb. New notebook written to student.ipynb.\n"
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


def test_solve():
    # TODO Add better tear down.
    output = subprocess.run(
        [
            "nbchkr",
            "solve",
            "--source",
            f"{NB_PATH}/test.ipynb",
            "--output",
            "solution.ipynb",
        ],
        capture_output=True,
    )
    expected_stdout = str.encode(
        f"Checks removed from {NB_PATH}/test.ipynb. New notebook written to solution.ipynb.\n"
    )
    assert output.stderr == b""
    assert output.stdout == expected_stdout

    student_nb = nbchkr.utils.read(nb_path="solution.ipynb")
    expected_length = 4
    assert type(student_nb["cells"]) is list
    assert len(student_nb["cells"]) == expected_length
    assert "assert" not in str(student_nb)
    assert "sum(i for i in range(11))" in str(student_nb)
    # TODO Add a better pytest cleanup.
    try:
        pathlib.Path("solution.ipynb").unlink()
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
    expected_outputs = [
        ["2", "10", "True", "False", "True", "False"],
        ["2", "10", "False", "False", "True", "False"],
        ["10", "10", "True", "True", "True", "True"],
    ]
    for submission_nb, expected_output in zip(submission_nbs, expected_outputs):
        output = subprocess.run(
            [
                "nbchkr",
                "check",
                "--source",
                f"{NB_PATH}/test.ipynb",
                "--submitted",
                f"{NB_PATH}/{submission_nb}",
                "--feedback-suffix",
                "_feedback.md",
                "--output",
                "output.csv",
            ],
            capture_output=True,
        )
        with open("output.csv", "r") as f:
            csv_reader = csv.reader(f)
            output = list(csv_reader)

        expected_output = [
            [
                "",
                "Submission filepath",
                "Score",
                "Maximum score",
                "Tags match",
                "Correct answer",
                "Has docstring",
                "Correct answer for n up until 10",
                "Run time",
            ],
            ["0", f"{NB_PATH}/{submission_nb}"] + expected_output,
        ]
        assert output[0] == expected_output[0], "Header is not written correctly"
        assert (
            output[1][:-1] == expected_output[1]
        ), "Expected output not written correctly"


def test_check_on_a_collection_of_notebooks():
    """
    Check that check can be run on a pattern of notebooks.

    Note that this also uses the default values for the outputs.
    """
    # TODO Add better tear down.
    output = subprocess.run(
        [
            "nbchkr",
            "check",
            "--source",
            f"{NB_PATH}/test.ipynb",
            "--submitted",
            f"{NB_PATH}/*.ipynb",
        ],
        capture_output=True,
    )

    with open("output.csv", "r") as f:
        csv_reader = csv.reader(f)
        output = list(csv_reader)

    expected_output_without_time = [
        [
            "",
            "Submission filepath",
            "Score",
            "Maximum score",
            "Tags match",
            "Correct answer",
            "Has docstring",
            "Correct answer for n up until 10",
        ],
        [
            "0",
            f"{NB_PATH}/submission.ipynb",
            "2",
            "10",
            "True",
            "False",
            "True",
            "False",
        ],
        [
            "1",
            f"{NB_PATH}/submission_with_missing_tags.ipynb",
            "2",
            "10",
            "False",
            "False",
            "True",
            "False",
        ],
        ["2", f"{NB_PATH}/test.ipynb", "10", "10", "True", "True", "True", "True"],
    ]

    for row, expected_row in zip(output, expected_output_without_time):
        assert row[:-1] == expected_row


def test_check_on_documentation_examples():
    """
    Note that this also serves as a test of the tutorial commands: if there is a
    regression that causes these tests to fail the documentation might need to
    be updated.

    This deletes the feedback files and checks they're created.
    """
    docs_path = f"{NB_PATH}/../../docs/tutorial/assignment"
    # TODO Add better tear down.

    submissions_directory = pathlib.Path(f"{docs_path}/submissions/")
    for feedback_path in submissions_directory.glob("*.ipynb-feedback.testmd"):
        feedback_path.unlink(missing_ok=True)

    output = subprocess.run(
        [
            "nbchkr",
            "check",
            "--source",
            f"{docs_path}/main.ipynb",
            "--submitted",
            f"{docs_path}/submissions/*.ipynb",
            "--feedback-suffix",
            "-feedback.testmd",
            "--output",
            "data.csv",
        ],
        capture_output=True,
    )

    with open("data.csv", "r") as f:
        csv_reader = csv.reader(f)
        output = list(csv_reader)

    expected_output_without_time = [
        [
            "",
            "Submission filepath",
            "Score",
            "Maximum score",
            "Tags match",
            "Integer answer",
            "Correct answer",
            "Presence of docstring",
        ],
        [
            "0",
            f"{docs_path}/submissions/assignment_01.ipynb",
            "2",
            "11",
            "True",
            "True",
            "False",
            "True",
        ],
        [
            "1",
            f"{docs_path}/submissions/assignment_02.ipynb",
            "10",
            "11",
            "True",
            "True",
            "True",
            "False",
        ],
        [
            "2",
            f"{docs_path}/submissions/assignment_03.ipynb",
            "4",
            "11",
            "False",
            "True",
            "False",
            "False",
        ],
    ]
    for row, expected_row in zip(output, expected_output_without_time):
        assert row[:-1] == expected_row

    number_of_feedback_files = 0

    for feedback_path in submissions_directory.glob("*.ipynb-feedback.testmd"):
        number_of_feedback_files += 1
        assert feedback_path.is_file()

    expected_number_of_feedback_files = 3
    assert number_of_feedback_files == expected_number_of_feedback_files


def test_check_on_a_non_notebook_file():
    """
    Tries to read in this test file.
    """
    # TODO add better tear down.

    submission_nb = __file__
    expected_output_without_time = ["", "", "False"]
    expected_feedback = (
        "\tYour notebook file was not in the correct format and could not be read"
    )

    output = subprocess.run(
        [
            "nbchkr",
            "check",
            "--source",
            f"{NB_PATH}/test.ipynb",
            "--submitted",
            f"{submission_nb}",
            "--feedback-suffix",
            "_feedback.md",
            "--output",
            "output.csv",
        ],
        capture_output=True,
    )
    print(output.stdout)
    expected_stdout = str.encode(f"Check 1/1: {submission_nb}\n")
    expected_stdout += str.encode(
        f"\t{submission_nb} checked against {NB_PATH}/test.ipynb. Feedback written to {submission_nb}_feedback.md and output written to output.csv.\n"
    )
    expected_stdout += str.encode(
        f"\tWARNING: {submission_nb} has tags that do not match the source.\n"
    )
    expected_stdout += str.encode(f"\tFinished in 0 seconds\n")
    assert output.stdout == expected_stdout

    with open("output.csv", "r") as f:
        csv_reader = csv.reader(f)
        output = list(csv_reader)

    expected_header = [
        "",
        "Submission filepath",
        "Score",
        "Maximum score",
        "Tags match",
        "Run time",
    ]
    expected_output_without_time = [
        "0",
        f"{submission_nb}",
    ] + expected_output_without_time
    assert output[0] == expected_header
    assert output[1][:-1] == expected_output_without_time
    assert float(output[1][-1]) > 0

    with open(f"{submission_nb}_feedback.md", "r") as f:
        feedback = f.read()
        assert feedback == expected_feedback

    # TODO Add a better pytest cleanup.
    try:
        pathlib.Path(f"{submission_nb}_feedback.md").unlink()
    except FileNotFoundError:  # TODO Ensure py3.8 is used so that can pass
        # `missing_ok=True` to `path.unlink`.
        pass
