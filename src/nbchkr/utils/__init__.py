import json
import re
import pathlib

from typing import Tuple, Optional

import nbformat  # type: ignore
from nbconvert.preprocessors import ExecutePreprocessor  # type: ignore

TAGS_REGEX_PATTERNS_TO_IGNORE = ["hide", r"score:\d"]
SOLUTION_REGEX = re.compile(
    r"### BEGIN SOLUTION[\s\S](.*?)[\s\S]### END SOLUTION", re.DOTALL
)
ANSWER_TAG_REGEX = r"answer:*"
SCORE_REGEX = re.compile(r"score:(\d+)")


def read(nb_path: pathlib.Path, as_version: int = 4) -> dict:
    """
    Read a jupyter notebook file at `nb_path`.

    Returns the python `dict` representation.
    """
    with open(nb_path, "r") as f:
        nb = nbformat.read(f, as_version=as_version)
    return nb


def remove_cells(
    nb_json, tags_regex_patterns_to_ignore=None, solution_regex=None
):  # TODO Add typing to this function
    """
    Given a dictionary representation of a notebook, removes:

    - Cells with tags matching patterns in `tags_regex_patterns_to_ignore`
    - Text in cells matching the `solution_regex` pattern.

    Returns the python `dict` representation.
    """
    if tags_regex_patterns_to_ignore is None:
        tags_regex_patterns_to_ignore = TAGS_REGEX_PATTERNS_TO_IGNORE
    if solution_regex is None:
        solution_regex = SOLUTION_REGEX
    cells = []
    for cell in nb_json["cells"]:
        if "tags" not in cell["metadata"] or all(
            not bool(re.match(pattern=pattern, string=tag))
            for tag in cell["metadata"]["tags"]
            for pattern in tags_regex_patterns_to_ignore
        ):
            try:
                source = "".join(cell["source"])
                new_source = re.sub(pattern=solution_regex, repl="", string=source)
                cell["source"] = new_source

                if bool(re.match(pattern=solution_regex, string=source)) is True:
                    try:
                        cell["outputs"] = []
                    except KeyError:  # pragma: no cover
                        pass  # TODO Add test coverage for this statement
            except KeyError:  # pragma: no cover
                pass  # TODO Add test coverage for this statement
            cells.append(cell)
    nb_json["cells"] = cells
    return nb_json


def write(output_path: pathlib.Path, nb_json):
    """
    Write the python dict representation of a notebook to `output_path`.
    """
    output_path.write_text(json.dumps(nb_json))


def add_checks(nb_json: dict, source_nb_json: dict, answer_tag_regex=None) -> dict:
    """
    Given a `nb_json` and a source `source_nb_json`, add the cells in
    `source_nb` with tags matching `answer_tag_regex` to `source_nb_json`

    This is used to add a student's answers to the source notebook.
    """
    if answer_tag_regex is None:
        answer_tag_regex = ANSWER_TAG_REGEX
    answers = {
        tag: cell
        for cell in nb_json["cells"]
        for tag in cell["metadata"].get("tags", [])
        if bool(re.match(pattern=answer_tag_regex, string=tag))
    }
    for i, cell in enumerate(source_nb_json["cells"]):
        for tag in cell["metadata"].get("tags", []):
            if tag in answers:
                source_nb_json["cells"][i] = answers[tag]
    return source_nb_json


def get_tags(cell: dict, tag_seperator: str = "|") -> Optional[str]:
    """
    Given a `cell` of a notebook, return a string with all tags separated by
    `|`.
    """
    try:
        return tag_seperator.join(cell["metadata"]["tags"])
    except KeyError:
        return None


def get_score(cell: dict, score_regex_pattern=None) -> int:
    """
    Given a `cell` of a notebook, return the score as defined by the
    `score_regex_pattern`.
    """
    if score_regex_pattern is None:
        score_regex_pattern = SCORE_REGEX
    tags = get_tags(cell)
    if tags is not None:
        search = re.search(pattern=score_regex_pattern, string=tags)
        try:
            return int(search.group(1))  # type: ignore
        except AttributeError:
            return 0
    return 0


def check(
    nb_node: dict, timeout: int = 600, score_regex_pattern=None
) -> Tuple[int, int, str]:
    """
    Given a `nb_node`, it executes the notebook and keep track of the score.

    This returns 3 things:

    - The student score
    - The total score obtainable
    - Some feedback in markdown format
    """
    if score_regex_pattern is None:
        score_regex_pattern = SCORE_REGEX

    ep = ExecutePreprocessor(timeout=timeout, allow_errors=True)
    ep.preprocess(nb_node)

    total_score = 0
    maximum_score = 0
    feedback_md = ""

    for cell in nb_node["cells"]:
        if get_score(cell) > 0:
            score = get_score(cell)
            maximum_score += score
            try:
                outputs = cell["outputs"][0]
                if outputs["output_type"] == "error":
                    question_feedback = outputs["evalue"]
                    feedback_md += f"""
{question_feedback}

0 / {score}
"""
            except IndexError:
                assertion = cell["source"]
                feedback_md += f"""
Assertion passed:

    {assertion}

{score} / {score}
"""
                total_score += score
    return total_score, maximum_score, feedback_md
