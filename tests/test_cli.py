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
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  check    This checks a given submission against a source.
  release  This releases a piece of coursework by removing the solutions...
"""
    assert output.stdout == expected_stdout
    assert output.stderr == b""


def test_release_help_call():
    output = subprocess.run(["nbchkr", "release", "--help"], capture_output=True)
    expected_stdout = b"""Usage: nbchkr release [OPTIONS]

  This releases a piece of coursework by removing the solutions from a
  source.

Options:
  --source PATH  The path to the source ipynb file  [required]
  --output PATH  The path to the destination ipynb file  [required]
  --help         Show this message and exit.
"""
    assert output.stdout == expected_stdout
    assert output.stderr == b""


def test_check_help_call():
    output = subprocess.run(["nbchkr", "check", "--help"], capture_output=True)
    expected_stdout = b"""Usage: nbchkr check [OPTIONS]

  This checks a given submission against a source.

Options:
  --source PATH           The path to the source ipynb file  [required]
  --submitted TEXT        The path pattern to the submitted ipynb file(s)
                          [required]

  --feedback-suffix TEXT  The suffix to add to the file name for the feedback
                          [required]

  --output PATH           The path to output comma separated value file
                          [required]

  --help                  Show this message and exit.
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
                "--feedback-suffix",
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
            "--feedback-suffix",
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


def test_check_on_documentation_exampless():
    """
    Note that this also serves as a test of the tutorial commands: if there is a
    regression that causes these tests to fail the documentation might need to
    be updated.
    """
    docs_path = f"{NB_PATH}/../../docs/tutorial/assignment"
    # TODO Add better tear down.
    output = subprocess.run(
        [
            "nbchkr",
            "check",
            "--source",
            f"{docs_path}/main.ipynb",
            "--submitted",
            f"{docs_path}/submissions/*.ipynb",
            "--feedback_suffix",
            "_feedback.testmd",
            "--output",
            "data.csv",
        ],
        capture_output=True,
    )

    with open("data.csv", "r") as f:
        csv_reader = csv.reader(f)
        output = list(csv_reader)

    expected_output = [
        ["Submission filepath", "Score", "Maximum score", "Tags match"],
        [f"{docs_path}/submissions/assignment_01.ipynb", "2", "11", "True"],
        [f"{docs_path}/submissions/assignment_02.ipynb", "10", "11", "True"],
        [f"{docs_path}/submissions/assignment_03.ipynb", "4", "11", "False"],
    ]
    assert output == expected_output

    submissions_directory = pathlib.Path(f"{docs_path}/submissions/")
    number_of_feedback_files = 0

    for feedback_path in submissions_directory.glob("*.ipynb_feedback.testmd"):
        number_of_feedback_files += 1
        expected_feedback_path = pathlib.Path(
            f"{docs_path}/submissions/{feedback_path.stem}.md"
        )
        feedback = feedback_path.read_text()
        expected_feedback = expected_feedback_path.read_text()
        assert feedback == expected_feedback

    expected_number_of_feedback_files = 3
    assert number_of_feedback_files == expected_number_of_feedback_files
