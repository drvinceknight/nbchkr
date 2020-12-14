import collections
import json
import pathlib
import re
from typing import Tuple, Union

import nbformat  # type: ignore
import unidecode  # type: ignore
from nbconvert.preprocessors import ExecutePreprocessor  # type: ignore

TAGS_REGEX_PATTERNS_TO_IGNORE = ["hide", r"score:\d"]
SOLUTION_REGEX = re.compile(
    r"### BEGIN SOLUTION[\s\S](.*?)[\s\S]### END SOLUTION", re.DOTALL
)
SOLUTION_REPL = r"""### BEGIN SOLUTION


### END SOLUTION"""
UNIVERSAL_REGEX = re.compile(r".", re.DOTALL)
ANSWER_TAG_REGEX = r"answer:*"
SCORE_REGEX = re.compile(r"score:(\d+)")
DESCRIPTION_REGEX = re.compile(r"description:(.*)")


def read(nb_path: Union[pathlib.Path, str], as_version: int = 4) -> dict:
    """
    Read a jupyter notebook file at `nb_path`.

    Returns the python `dict` representation.
    """
    with open(nb_path, "r") as f:
        nb = nbformat.read(f, as_version=as_version)
    return nb


def remove_cells(
    nb_node, tags_regex_patterns_to_ignore=None, solution_regex=None, solution_repl=None
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
    if solution_repl is None:
        solution_repl = SOLUTION_REPL
    cells = []
    for cell in nb_node["cells"]:
        if "tags" not in cell["metadata"] or all(
            not bool(re.match(pattern=pattern, string=tag))
            for tag in cell["metadata"]["tags"]
            for pattern in tags_regex_patterns_to_ignore
        ):
            try:
                source = unidecode.unidecode("".join(cell["source"]))
                new_source = re.sub(
                    pattern=solution_regex, repl=solution_repl, string=source
                )
                cell["source"] = new_source

                if solution_repl in cell["source"]:
                    if "outputs" in cell.keys():
                        cell["outputs"] = []
            except KeyError:  # pragma: no cover
                pass  # TODO Add test coverage for this statement
            cells.append(cell)
    nb_node["cells"] = cells
    return nb_node


def write(output_path: pathlib.Path, nb_node: dict):
    """
    Write the python dict representation of a notebook to `output_path`.
    """
    output_path.write_text(json.dumps(nb_node))


def add_checks(nb_node: dict, source_nb_node: dict, answer_tag_regex=None) -> dict:
    """
    Given a `nb_node` and a source `source_nb_node`, add the cells in
    `nb_node` with tags matching `answer_tag_regex` to `source_nb_node`

    This is used to add a student's answers to the source notebook.
    """
    if answer_tag_regex is None:
        answer_tag_regex = ANSWER_TAG_REGEX

    answers = {
        tag: cell
        for cell in nb_node["cells"]
        for tag in cell["metadata"].get("tags", [])
        if bool(re.match(pattern=answer_tag_regex, string=tag))
    }

    for i, cell in enumerate(source_nb_node["cells"]):
        for tag in cell["metadata"].get("tags", []):
            if tag in answers:
                source_nb_node["cells"][i] = answers[tag]
            elif bool(re.match(pattern=answer_tag_regex, string=tag)):
                source_nb_node["cells"][i]["source"] = ""

    return source_nb_node


def get_tags(cell: dict, tag_seperator: str = "|", tag_regex=None) -> str:
    """
    Given a `cell` of a notebook, return a string with all tags that match
    `tag_regex` separated by `|`.
    """
    if tag_regex is None:
        tag_regex = UNIVERSAL_REGEX
    try:
        return tag_seperator.join(
            [
                tag
                for tag in cell["metadata"]["tags"]
                if bool(re.match(pattern=tag_regex, string=tag))
            ]
        )
    except KeyError:
        return ""


def get_score(cell: dict, score_regex_pattern=None) -> int:
    """
    Given a `cell` of a notebook, return the score as defined by the
    `score_regex_pattern`.
    """
    if score_regex_pattern is None:
        score_regex_pattern = SCORE_REGEX
    tags = get_tags(cell)
    if tags != "":
        search = re.search(pattern=score_regex_pattern, string=tags)
        try:
            return int(search.group(1))  # type: ignore
        except AttributeError:
            return 0
    return 0


def get_description(
    cell: dict, description_regex_pattern=None, tag_seperator: str = "|"
) -> str:
    """
    Given a `cell` of a notebook, return the description as defined by the
    `description_regex_pattern`.
    """
    if description_regex_pattern is None:
        description_regex_pattern = DESCRIPTION_REGEX
    tags = get_tags(cell, tag_seperator=tag_seperator)
    if tags != "":
        for tag in tags.split(tag_seperator):
            search = re.search(pattern=description_regex_pattern, string=tag)
            try:
                return search.group(1).replace("-", " ").capitalize()  # type: ignore
            except AttributeError:
                pass
    return ""


def check(
    nb_node: dict,
    timeout: int = 600,
    score_regex_pattern=None,
    answer_tag_pattern=None,
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
    if answer_tag_pattern is None:
        answer_tag_pattern = ANSWER_TAG_REGEX
    ep = ExecutePreprocessor(timeout=timeout, allow_errors=True)
    ep.preprocess(nb_node)

    total_score = 0
    maximum_score = 0
    feedback_md = ""

    for cell in nb_node["cells"]:
        answer_tags = get_tags(cell=cell, tag_regex=answer_tag_pattern)
        if (
            answer_tags is not None
            and len(get_tags(cell=cell, tag_regex=answer_tag_pattern)) > 0
        ):
            feedback_md += f"""
---

## {answer_tags}
"""
        # TODO Use the walrus operator here.
        if get_score(cell, score_regex_pattern=score_regex_pattern) > 0:
            score = get_score(cell)
            description = get_description(cell)
            if description != "":
                feedback_md += f"""
### {description}
"""
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
                feedback_md += f"""
{score} / {score}
"""
                total_score += score
    return total_score, maximum_score, feedback_md


def check_tags_match(
    source_nb_node: dict,
    nb_node: dict,
    tag_seperator: str = "|",
    tag_regex=None,
) -> bool:
    """
    This checks if the count of tags that match `tag_regex` on each cell matches. Note that it does not
    necessarily guarantee that the tags are on the same cells.
    """
    if tag_regex is None:
        tag_regex = ANSWER_TAG_REGEX
    source_nb_tags = [
        get_tags(cell, tag_seperator=tag_seperator, tag_regex=tag_regex)
        for cell in source_nb_node["cells"]
    ]
    nb_tags = [
        get_tags(cell, tag_seperator=tag_seperator, tag_regex=tag_regex)
        for cell in nb_node["cells"]
    ]

    # TODO I do not really understand why the `["", None]` is required here.
    # This is unwanted behaviour from `get_tags` which is returning empty tags.
    # Aim to remove this.`
    source_nb_tag_counter = collections.Counter(
        [tag for tag in source_nb_tags if tag not in ["", None]]
    )
    nb_tag_counter = collections.Counter(
        [tag for tag in nb_tags if tag not in ["", None]]
    )
    return source_nb_tag_counter == nb_tag_counter
